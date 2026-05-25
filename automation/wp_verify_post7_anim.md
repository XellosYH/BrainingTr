# WP Page #303 라이브 검증 + 롤백 가이드 — Post #7 민화투 카드 인식 애니메이션

**생성**: 2026-05-25 / dev v6.55
**대상**: `https://neuralcare.co.kr/brain-games/minwhatoo/` (WP Page ID: 303)
**사용 시점**: 사용자 PATCH 직후 브라우저 F12 → Console에서 실행
**기준 버전**: 위젯 헤더 주석 `v3.45 / 2026-05-25` 확인됨

---

## 실행 순서 안내

```
PATCH 완료
    ↓
1단계: 페이지 새로고침 (F5)
    ↓
2단계: F12 → Console → [섹션 1 통합 검증 스니펫] 붙여넣기 + 실행
    ↓
3단계: 결과 표 확인 (전부 PASS면 완료 / FAIL 있으면 섹션 3 롤백 가이드)
    ↓
4단계: 동적 시나리오 검증 (섹션 2 체크리스트 — 게임 1판 플레이)
    ↓
전부 PASS → 섹션 4 git 가이드 (lead 승인 필수)
```

---

## 섹션 1: 라이브 검증 통합 스니펫 (PATCH 직후 콘솔 1회 실행)

> ⚠️ **반드시 페이지 새로고침(F5) 후 실행** — PATCH 전 페이지에서 실행하면 구버전 JS가 로드된 상태라 SW 결과가 틀릴 수 있습니다.

아래 스니펫 전체를 복사해서 콘솔에 한 번에 붙여넣으세요. 자동으로 결과 표를 출력합니다.

```js
(function() {
  var 결과 = [];

  // ──────────────────────────────────────────────
  // S1: 게임 허브 페이지 예외 — 면제
  // ──────────────────────────────────────────────
  결과.push({ 항목: 'S1', 설명: '본문 500자 확인', 판정: 'SKIP', 비고: '게임 허브 페이지 예외 — 면제' });

  // ──────────────────────────────────────────────
  // S3: 한글 Mojibake 0건 확인
  // ──────────────────────────────────────────────
  var 본문텍스트 = document.body.innerText || '';
  var 모지바케패턴 = /[ëìíîïãâàáÃÂ]/g;
  var 모지바케건수 = (본문텍스트.match(모지바케패턴) || []).length;
  결과.push({
    항목: 'S3',
    설명: 'Mojibake 0건 (ë·ì·í·ã 패턴)',
    판정: 모지바케건수 === 0 ? 'PASS' : 'FAIL',
    비고: '검출 건수: ' + 모지바케건수
  });

  // ──────────────────────────────────────────────
  // SW1: BH_animateCardReveal 함수 존재
  // ──────────────────────────────────────────────
  결과.push({
    항목: 'SW1',
    설명: 'BH_animateCardReveal === function',
    판정: typeof BH_animateCardReveal === 'function' ? 'PASS' : 'FAIL',
    비고: '현재 타입: ' + typeof BH_animateCardReveal
  });

  // ──────────────────────────────────────────────
  // SW2: BH_animateCapture 함수 존재
  // ──────────────────────────────────────────────
  결과.push({
    항목: 'SW2',
    설명: 'BH_animateCapture === function',
    판정: typeof BH_animateCapture === 'function' ? 'PASS' : 'FAIL',
    비고: '현재 타입: ' + typeof BH_animateCapture
  });

  // ──────────────────────────────────────────────
  // SW3: BH_ANIM_SPEED 객체 존재
  // ──────────────────────────────────────────────
  var sw3_pass = typeof BH_ANIM_SPEED === 'object' && BH_ANIM_SPEED !== null &&
                 typeof BH_ANIM_SPEED.normal === 'object';
  결과.push({
    항목: 'SW3',
    설명: 'BH_ANIM_SPEED === object (slow/normal/fast)',
    판정: sw3_pass ? 'PASS' : 'FAIL',
    비고: sw3_pass ? 'normal.REVEAL=' + (BH_ANIM_SPEED.normal && BH_ANIM_SPEED.normal.REVEAL) : '미정의 또는 구조 불일치'
  });

  // ──────────────────────────────────────────────
  // SW4: BH_startWithDiff 함수 존재 (회귀 확인)
  // ──────────────────────────────────────────────
  결과.push({
    항목: 'SW4',
    설명: 'BH_startWithDiff === function (회귀 확인)',
    판정: typeof BH_startWithDiff === 'function' ? 'PASS' : 'FAIL',
    비고: '현재 타입: ' + typeof BH_startWithDiff
  });

  // ──────────────────────────────────────────────
  // SW5: BH_skipAnim 함수 존재
  // ──────────────────────────────────────────────
  결과.push({
    항목: 'SW5',
    설명: 'BH_skipAnim === function',
    판정: typeof BH_skipAnim === 'function' ? 'PASS' : 'FAIL',
    비고: '현재 타입: ' + typeof BH_skipAnim
  });

  // ──────────────────────────────────────────────
  // A13: 48장 카드 type↔svgUrl mismatch 0건
  // ──────────────────────────────────────────────
  if (typeof BH_DECK_DATA !== 'undefined') {
    var 전체카드 = BH_DECK_DATA.length;
    var 미스매치 = BH_DECK_DATA.filter(function(c) {
      return !c.type || !c.svgUrl || c.svgUrl === '';
    }).length;
    결과.push({
      항목: 'A13',
      설명: '48장 카드 type↔svgUrl mismatch 0건',
      판정: (전체카드 === 48 && 미스매치 === 0) ? 'PASS' : 'FAIL',
      비고: '전체: ' + 전체카드 + '장 / mismatch: ' + 미스매치 + '건'
    });
  } else {
    결과.push({ 항목: 'A13', 설명: '48장 카드 mismatch 0건', 판정: 'FAIL', 비고: 'BH_DECK_DATA 미정의 — SW1·SW2 FAIL과 연동' });
  }

  // ──────────────────────────────────────────────
  // Q8: #BH_overlay_card DOM 존재 확인
  // ──────────────────────────────────────────────
  var 오버레이요소 = document.getElementById('BH_overlay_card') ||
                    document.querySelector('.BH_overlay_card');
  결과.push({
    항목: 'Q8',
    설명: '#BH_overlay_card 또는 .BH_overlay_card DOM 존재',
    판정: 오버레이요소 ? 'PASS' : 'FAIL',
    비고: 오버레이요소 ? '요소 발견: ' + (오버레이요소.id || 오버레이요소.className) : '요소 없음 — 위젯 구조 확인 필요'
  });

  // ──────────────────────────────────────────────
  // Q11: #BH_anim_live aria-live div 존재
  // ──────────────────────────────────────────────
  var 아리아요소 = document.getElementById('BH_anim_live');
  결과.push({
    항목: 'Q11',
    설명: '#BH_anim_live aria-live div 존재',
    판정: 아리아요소 ? 'PASS' : 'FAIL',
    비고: 아리아요소 ? 'aria-live=' + 아리아요소.getAttribute('aria-live') : '요소 없음'
  });

  // ──────────────────────────────────────────────
  // HDR: 헤더 주석 v3.45 + 2026-05-25 확인 (구버전 0건)
  // ──────────────────────────────────────────────
  var 페이지HTML = document.documentElement.outerHTML;
  var hdr_v345  = 페이지HTML.includes('v3.45');
  var hdr_date  = 페이지HTML.includes('2026-05-25');
  var hdr_v5b   = 페이지HTML.includes('v5b');
  var hdr_v343  = 페이지HTML.includes('v3.43');
  var hdr_pass  = hdr_v345 && hdr_date && !hdr_v5b && !hdr_v343;
  결과.push({
    항목: 'HDR',
    설명: '헤더 주석 v3.45 + 2026-05-25 포함 / v5b·v3.43 0건',
    판정: hdr_pass ? 'PASS' : (hdr_v345 && hdr_date ? 'WARN' : 'FAIL'),
    비고: 'v3.45=' + hdr_v345 + ' / 2026-05-25=' + hdr_date + ' / v5b잔존=' + hdr_v5b + ' / v3.43잔존=' + hdr_v343
  });

  // ──────────────────────────────────────────────
  // 결과 출력
  // ──────────────────────────────────────────────
  var 전체통과 = 결과.filter(function(r) { return r.판정 !== 'SKIP'; })
                    .every(function(r) { return r.판정 === 'PASS' || r.판정 === 'WARN'; });
  var FAIL건수 = 결과.filter(function(r) { return r.판정 === 'FAIL'; }).length;

  console.log('');
  console.log('══════════════════════════════════════════════════');
  console.log('  라이브 검증 결과 — Post #7 민화투 카드 애니메이션');
  console.log('══════════════════════════════════════════════════');
  결과.forEach(function(r) {
    var 아이콘 = r.판정 === 'PASS' ? '✅' : r.판정 === 'SKIP' ? '⏭️' : r.판정 === 'WARN' ? '⚠️' : '❌';
    console.log(아이콘 + ' [' + r.항목 + '] ' + r.설명);
    console.log('   → ' + r.비고);
  });
  console.log('');
  console.log('──────────────────────────────────────────────────');
  if (FAIL건수 === 0) {
    console.log('✅ 전체 PASS — 동적 시나리오 검증(섹션 2)으로 진행하세요');
  } else {
    console.log('❌ FAIL ' + FAIL건수 + '건 발견 — 섹션 3 롤백 가이드를 확인하세요');
  }
  console.log('══════════════════════════════════════════════════');
})();
```

---

## 섹션 2: 동적 시나리오 검증 — 게임 1판 플레이 체크리스트 (사용자 육안 확인)

아래 체크리스트를 출력하거나 메모지에 적어두고, 게임을 1판 직접 플레이하며 확인하세요.

```
──────────────────────────────────────────────
  동적 시나리오 확인 체크리스트 (게임 1판)
──────────────────────────────────────────────

[게임 시작 전]
□ Q1-준비  난이도 선택 모달이 정상 표시되는가?
           (화면 중앙에 쉬움/보통/어려움 버튼 보임)
□ Q6-준비  속도 선택 버튼(느림/보통/빠름)이 모달 하단에 보이는가?

[플레이어 손패 내기 — 매치 있는 경우]
□ Q1       손패 카드를 선택하면 → 카드가 확대되어 중앙에 보이는가? (800ms 정도 보임)
□ Q1       확대된 카드가 바닥 매치 카드 옆으로 이동했다가 내 획득 칸으로 이동하는가?

[플레이어 손패 내기 — 매치 없는 경우]
□ Q2       매치가 없으면 → 카드가 확대 후 바닥에 내려앉는가?

[더미 뒤집기]
□ Q3       더미 카드가 뒤집어지면 → 확대 표시 후 매치 처리가 보이는가?
□ Q4       더미 카드가 매치 없으면 → 바닥에 내려앉은 뒤 AI 턴으로 넘어가는가?

[AI 턴 관찰]
□ Q5       AI 턴이 진행될 때 → AI 패가 확대 표시되어 어떤 패를 냈는지 보이는가?
           (플레이어 턴보다 빠르게 진행되면 정상)

[속도 설정 확인 — 별도 판 권장]
□ Q6       "느림" 선택 후 플레이 → 각 단계가 눈에 띄게 느린가?
□ Q7       "빠름" 선택 후 플레이 → 각 단계가 눈에 띄게 빠른가?

[클릭 skip 확인]
□ Q8       카드가 확대 애니메이션 중일 때 게임판을 탭/클릭하면 →
           애니메이션이 건너뛰어지는가?

[족보 달성 시]
□ Q12      족보(5월 다섯장 등)를 완성했을 때 → 효과음이 겹치지 않고 순서대로 나는가?

[게임 마무리]
□ Q13      마지막 카드를 획득하고 → 결과 화면이 자연스럽게 나타나는가?
           (애니메이션 완료 후 결과 화면 진입)

──────────────────────────────────────────────
모든 항목 □ 체크 완료 → 동적 검증 PASS
1개라도 이상하면 → 아래 내용을 lead에게 알려주세요:
  "Q{번호}: {어떤 문제가 있었는지 1줄 설명}"
──────────────────────────────────────────────
```

---

## 섹션 3: 롤백 가이드 (PATCH 실패 또는 섹션 1 FAIL 시)

### 상황 A: window.__BH_backup_raw가 아직 메모리에 있는 경우

PATCH 직후 같은 탭에서 페이지를 닫지 않았다면, 백업 변수가 메모리에 남아 있습니다.

```js
// 롤백 스니펫 — 1줄 실행으로 이전 버전 복원
// ※ 반드시 PATCH에 사용했던 같은 탭에서 실행 (변수가 같은 탭 메모리에 있어야 함)
(async function() {
  if (!window.__BH_backup_raw) {
    console.error('❌ 백업 변수(window.__BH_backup_raw)가 없습니다.');
    console.error('   → 페이지를 닫았거나 새로고침했으면 아래 "상황 B"를 사용하세요.');
    return;
  }

  // Nonce 만료 시 재발급 (롤백에도 Nonce 필요)
  var nonceResp = await fetch('/wp-admin/admin-ajax.php?action=rest-nonce', {
    credentials: 'include'
  });
  var freshNonce = (await nonceResp.text()).trim();
  if (!freshNonce || freshNonce === 'false' || freshNonce.length < 5) {
    console.error('❌ Nonce 발급 실패 — wp-admin에 로그인 후 다시 시도하세요.');
    return;
  }
  console.log('Nonce 재발급 완료 (앞 10자):', freshNonce.slice(0, 10) + '...');

  // 롤백 PATCH 전송
  var rollbackResp = await fetch('/wp-json/wp/v2/pages/303', {
    method: 'POST',
    headers: {
      'X-WP-Nonce': freshNonce,
      'Content-Type': 'application/json'
    },
    credentials: 'include',
    body: JSON.stringify({ content: window.__BH_backup_raw })
  });

  if (!rollbackResp.ok) {
    var errText = await rollbackResp.text();
    console.error('❌ 롤백 PATCH 실패:', rollbackResp.status, rollbackResp.statusText);
    console.error('오류 내용:', errText.slice(0, 300));
    console.error('→ 아래 "상황 C" WP 관리자 이전 버전 복원을 사용하세요.');
    return;
  }

  var result = await rollbackResp.json();
  console.log('✅ 롤백 완료 — Page ID:', result.id, '/ 상태:', result.status);
  console.log('페이지를 새로고침(F5)하여 이전 버전이 복원되었는지 확인하세요.');
})();
```

---

### 상황 B: Nonce만 만료된 경우 (변수는 있음)

Nonce + 롤백을 한 번에 처리하는 통합 스니펫 (위 상황 A 스니펫이 이미 포함하고 있습니다).
상황 A 스니펫을 그대로 실행하면 Nonce를 자동으로 재발급 후 롤백합니다.

---

### 상황 C: 탭을 닫았거나 새로고침해서 백업 변수가 없는 경우

WP 관리자 이전 버전 복원을 사용합니다.

```
1. https://neuralcare.co.kr/wp-admin/ 접속
2. 왼쪽 메뉴 → 페이지 → 모든 페이지
3. "두뇌 게임 — 민화투" (또는 brain-games/minwhatoo) 페이지 클릭
4. 오른쪽 패널 → "리비전(이전 버전)" 또는 영문 "Revisions" 클릭
5. 타임라인 슬라이더로 PATCH 직전 버전 선택
6. "이 버전 복원" 클릭
7. "업데이트" 클릭
```

---

### 상황 D: 섹션 1 SW FAIL — 위젯 함수 미로드 (위젯 자체 문제)

섹션 1에서 SW1~SW5 중 FAIL이 있고, 롤백 후에도 함수가 없다면:

```
1. WP 관리자 → 페이지 → 편집 모드
2. F12 → Console에서 아래 실행:

   document.querySelectorAll('script').forEach(function(s) {
     if (!s.src) console.log('인라인 스크립트 길이:', s.textContent.length);
   });

3. 길이 0 또는 현저히 짧은 스크립트 발견 시 → wpautop 오염 의심
4. lead에게 "인라인 스크립트 길이: N자" 보고 → dev 에이전트 재업로드 지시
```

---

## 섹션 4: git push 결정 가이드 (라이브 검증 PASS 후)

> ⚠️ **이 섹션은 lead 승인 + 사용자 명시 지시 없이는 절대 실행하지 마세요.**
> git 명령은 Claude Code(Windows) 환경에서만 실행합니다. 브라우저 콘솔에서 실행 불가.

### 전제 조건 (전부 PASS여야 git 작업 진행 가능)

```
□ 섹션 1 통합 스니펫 — FAIL 0건
□ 섹션 2 동적 체크리스트 — 전 항목 체크
□ lead 승인 메시지 확인
□ 사용자 "git push 진행해"와 같은 명시적 지시 확인
```

### git 작업 순서 (조건 충족 시 Claude Code 터미널에서 실행)

```powershell
# 1단계: 현재 상태 확인
git status
git log --oneline -5

# 2단계: 위젯 파일 스테이징
git add widgets/post7_widget.html

# 3단계: 커밋 (메시지는 lead 지시에 따름)
# git commit -m "feat(post7): 카드 인식 애니메이션 WP Page #303 PATCH 완료 — v3.45 라이브 적용"

# 4단계: push (사용자 명시 지시 후)
# git push origin main
```

> ❌ 이 섹션의 명령어는 사용자가 직접 실행하거나, Claude Code에서 "git push 진행해"와 같이 명시적으로 지시한 경우에만 실행합니다.
> 자동 실행, 조건부 실행 전부 금지.

---

## 빠른 참조 — 항목별 FAIL 대응표

| 항목 | FAIL 시 원인 | 대응 |
|---|---|---|
| S3 Mojibake | Base64 atob() 오류 또는 인코딩 문제 | Phase 2 TextDecoder 방식으로 재PATCH |
| SW1 BH_animateCardReveal | 위젯 JS 미로드 | wpautop 오염 확인 → 재업로드 |
| SW2 BH_animateCapture | 위젯 JS 미로드 | 동일 |
| SW3 BH_ANIM_SPEED | 속도 객체 미정의 | 동일 |
| SW4 BH_startWithDiff (회귀) | 구버전 덮어쓰기 위험 | 즉시 롤백 후 위젯 파일 정본 확인 |
| SW5 BH_skipAnim | skip 함수 누락 | 위젯 재업로드 |
| A13 카드 mismatch | BH_DECK_DATA 손상 또는 48장 미만 | 위젯 재업로드 |
| Q8 오버레이 요소 | HTML 구조 미삽입 | 위젯 재업로드 |
| Q11 aria-live | 접근성 요소 누락 | 위젯 재업로드 |
| HDR v5b·v3.43 잔존 | 구버전 wp:html 블록이 2개 이상 | raw에서 중복 블록 제거 후 재PATCH |

---

*생성: dev v6.55 / 2026-05-25*
*대상: Page ID 303 / 위젯 정본 v3.45 (85,025 bytes)*
*참고 문서: wp_patch_post7_anim.md / post7_card_animation_plan.md / post7_animation_qa_report.md*
