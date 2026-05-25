# WP PATCH Post7 — D-only (BH_doAITurn guard) 삽입 스니펫

- **작성일**: 2026-05-25
- **작성자**: dev 에이전트 v6.55
- **목적**: 라이브 Page #303 민화투 위젯의 `BH_doAITurn` 함수 진입부에 phase guard 삽입
- **전 단계 결과**:
  - A·B·C PATCH 완료 (라이브 반영)
  - D (doAITurn guard): OLD_D literal indexOf -1 → SKIP 상태
  - 라이브 raw length (C 반영 후): 83,750
  - 직전 진단: `function BH_doAITurn(){` 위치 = index 71529 확인

---

## 1. 상황 분석

직전 세션에서 v5 스니펫의 `OLD_D` literal string이 라이브 raw와 불일치해 indexOf -1 반환.
원인: C 적용 후 raw 내부 char 변형 또는 직전 패치 시도 중 미세 escape 차이 가능성.

**해결 전략**: literal string replace를 완전히 포기하고, 함수 시작부 `{` 직후 위치를
substring 슬라이싱으로 계산해 삽입. indexOf 대상을 `function BH_doAITurn(){`으로 단순화.

---

## 2. 메인 스니펫 (단일 IIFE — 콘솔 1회 붙여넣기)

아래 코드를 WP 관리자가 열려있는 Chrome 콘솔에 붙여넣어 실행.

```javascript
(async () => {
  // --- STEP 1: nonce 발급 ---
  const nonceRes = await fetch('/wp-admin/admin-ajax.php?action=rest-nonce', {credentials: 'include'});
  const nonce = await nonceRes.text();
  console.log('[D] nonce:', nonce.slice(0, 8) + '...');

  // --- STEP 2: 라이브 raw GET ---
  const pageRes = await fetch('/wp-json/wp/v2/pages/303?context=edit', {
    headers: {'X-WP-Nonce': nonce},
    credentials: 'include',
    cache: 'no-store'
  });
  const page = await pageRes.json();
  let raw = page.content.raw;
  console.log('[D] raw length (before):', raw.length);

  // --- STEP 3: BH_doAITurn 위치 찾기 (substring 기반) ---
  const TARGET = 'function BH_doAITurn(){';
  const GUARD  = "if(BH_GS.phase!=='AI_TURN')return;";
  const iD = raw.indexOf(TARGET);
  if (iD === -1) {
    console.error('[D] FAIL: BH_doAITurn 함수를 찾을 수 없음. 라이브 raw 상태 확인 필요.');
    return;
  }
  const iDend = iD + TARGET.length;  // { 직후 위치
  console.log('[D] BH_doAITurn index:', iD, '/ insertion point:', iDend);

  // --- STEP 4: 이미 가드 있으면 SKIP ---
  const lookahead = raw.slice(iDend, iDend + 40);
  if (lookahead.includes("phase!=='")) {
    console.log('[D] SKIP: 가드 이미 존재 -', lookahead.slice(0, 40));
    return;
  }

  // --- STEP 5: 가드 삽입 (substring 슬라이싱) ---
  const newRaw = raw.slice(0, iDend) + GUARD + raw.slice(iDend);
  console.log('[D] raw length (after):', newRaw.length, '/ delta:', newRaw.length - raw.length);
  console.log('[D] 삽입 확인 (iD~iD+80):', newRaw.slice(iD, iD + 80));

  // --- STEP 6: PATCH ---
  const patchRes = await fetch('/wp-json/wp/v2/pages/303', {
    method: 'POST',
    headers: {
      'X-WP-Nonce': nonce,
      'Content-Type': 'application/json'
    },
    credentials: 'include',
    body: JSON.stringify({content: newRaw})
  });
  const patchData = await patchRes.json();
  console.log('[D] PATCH status:', patchRes.status);

  // --- STEP 7: GET 재확인 ---
  const verifyRes = await fetch('/wp-json/wp/v2/pages/303?context=edit', {
    headers: {'X-WP-Nonce': nonce},
    credentials: 'include',
    cache: 'no-store'
  });
  const verifyPage = await verifyRes.json();
  const verifyRaw = verifyPage.content.raw;
  const verifyIdx = verifyRaw.indexOf(TARGET);
  const verifyLook = verifyIdx !== -1 ? verifyRaw.slice(verifyIdx, verifyIdx + 80) : 'NOT FOUND';

  console.log('[D] VERIFY raw length:', verifyRaw.length);
  console.log('[D] VERIFY phase guard present:', verifyLook.includes("phase!=='"));
  console.log('[D] VERIFY slice (iD~iD+80):', verifyLook);
  console.log('[D] DONE');
})();
```

---

## 3. 기대 콘솔 출력

```
[D] nonce: abc12345...
[D] raw length (before): 83750
[D] BH_doAITurn index: 71529 / insertion point: 71552
[D] raw length (after): 83784 / delta: 34
[D] 삽입 확인 (iD~iD+80): function BH_doAITurn(){if(BH_GS.phase!=='AI_TURN')return;if(BH_GS.aiHand.leng
[D] PATCH status: 200
[D] VERIFY raw length: 83784
[D] VERIFY phase guard present: true
[D] VERIFY slice (iD~iD+80): function BH_doAITurn(){if(BH_GS.phase!=='AI_TURN')return;if(BH_GS.aiHand.leng
[D] DONE
```

**주요 수치**:
- delta: +34 (가드 문자열 `if(BH_GS.phase!=='AI_TURN')return;` = 34자)
- VERIFY phase guard present: true = PASS

---

## 4. Fallback 분할 블록 (메인 스니펫 실패 시)

### Fallback A — nonce만 별도 실행 (세션 만료 대비)

```javascript
// BLOCK A: nonce 발급
fetch('/wp-admin/admin-ajax.php?action=rest-nonce', {credentials: 'include'})
  .then(r => r.text())
  .then(n => { window._bhNonce = n; console.log('[A] nonce ok:', n.slice(0,8)); });
```

### Fallback B — raw GET + 삽입 계산만 (PATCH 없이 미리 확인)

```javascript
// BLOCK B: raw 취득 + 위치 확인 (PATCH 없음)
(async () => {
  const r = await fetch('/wp-json/wp/v2/pages/303?context=edit', {
    headers: {'X-WP-Nonce': window._bhNonce},
    credentials: 'include',
    cache: 'no-store'
  });
  const p = await r.json();
  const raw = p.content.raw;
  window._bhRaw = raw;
  const iD = raw.indexOf('function BH_doAITurn(){');
  const iDend = iD + 'function BH_doAITurn(){'.length;
  const lookahead = raw.slice(iDend, iDend + 40);
  console.log('[B] raw.length:', raw.length);
  console.log('[B] iD:', iD, '/ iDend:', iDend);
  console.log('[B] lookahead:', lookahead);
  console.log('[B] guard already?', lookahead.includes("phase!=='"));
})();
```

### Fallback C — PATCH만 (B 실행 후, window._bhRaw 확보 상태에서)

```javascript
// BLOCK C: 가드 삽입 + PATCH
(async () => {
  const TARGET = 'function BH_doAITurn(){';
  const GUARD  = "if(BH_GS.phase!=='AI_TURN')return;";
  const raw = window._bhRaw;
  const iD = raw.indexOf(TARGET);
  const iDend = iD + TARGET.length;
  const newRaw = raw.slice(0, iDend) + GUARD + raw.slice(iDend);
  console.log('[C] delta:', newRaw.length - raw.length);
  const res = await fetch('/wp-json/wp/v2/pages/303', {
    method: 'POST',
    headers: {'X-WP-Nonce': window._bhNonce, 'Content-Type': 'application/json'},
    credentials: 'include',
    body: JSON.stringify({content: newRaw})
  });
  console.log('[C] status:', res.status);
  const data = await res.json();
  console.log('[C] saved length:', data.content && data.content.raw ? data.content.raw.length : 'N/A');
})();
```

---

## 5. PATCH 후 사용자 육안 확인 절차

PATCH 성공(status 200 + VERIFY phase guard present: true) 이후:

1. **라이브 페이지 새로고침**: `https://neuralcare.co.kr/brain-games/minwhatoo/` 열기 (캐시 무력화: Ctrl+Shift+R)
2. **난이도 선택**: 화면에서 "쉬움" 또는 "보통" 버튼 클릭
3. **게임 시작 후 대기**: 플레이어 턴 종료 후 **AI 자동 플레이가 일어나지 않음** 확인
   - PASS: 플레이어 카드를 낸 후 AI 턴이 자동 실행되지 않고 대기 상태 유지
   - FAIL: AI 턴이 자동 실행되거나 콘솔에 오류 발생
4. **콘솔 확인**: `typeof BH_doAITurn === 'function'` → `true` (함수 로드 정상)
5. **phase guard 확인**: 콘솔에서 `BH_GS.phase` 값 출력 — 게임 중 `'AI_TURN'` 아닐 때 BH_doAITurn 호출해도 즉시 return됨

---

## 6. 변경 요약

| 항목 | 내용 |
|---|---|
| 대상 | Page ID 303 (`/brain-games/minwhatoo/`) |
| 변경 위치 | `function BH_doAITurn(){` 직후 (index ~71552) |
| 삽입 문자열 | `if(BH_GS.phase!=='AI_TURN')return;` (34자) |
| 예상 raw 증가 | +34 (83750 → 83784) |
| 정본 파일 | 수정 금지 (git 관리) |
| 라이브 직접 PATCH | 사용자 콘솔 실행 후 진행 |
