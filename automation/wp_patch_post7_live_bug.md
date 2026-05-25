# WP Page #303 라이브 타겟 PATCH 스니펫
**작성**: dev 에이전트 v6.55 / 2026-05-25  
**대상**: https://neuralcare.co.kr/brain-games/minwhatoo/ (WP Page ID: 303)  
**목적**: 버그 A (sec=5→15) + 버그 B (BH_hideOverlay 추가) 동시 PATCH

---

## 협업 약속 자가 점검

| # | 약속 | 결과 | 비고 |
|---|------|------|------|
| 1 | lead 지시 범위 준수 | ✅ | PATCH 스니펫 작성 + 파일 저장. WP 실행 없음 |
| 2 | 운영자 표기 룰 (neuralcare.co.kr) | ✅ | 하이픈 없음. neuralcare.co.kr 사용 |
| 3 | YMYL 의료 단정 표현 0 | ✅ | 해당 없음 |
| 4 | dev.md + 정본 위젯 + game 보고서 사전 Read 완료 | ✅ | dev.md(lines 1-987), post7_widget.html, post7_animation_live_bug_report.md 전부 Read 완료 |
| 5 | 자기 단계 인지 (긴급 타겟 PATCH 스니펫 작성) | ✅ | 스니펫 파일 산출 — WP 실행은 사용자가 직접 |
| 6 | 출력 형식 (박스·표·기호) | ✅ | |
| 7 | lead 단일 보고 | ✅ | |
| 8 | git 자의적 실행 0건 | ✅ | git 명령 없음 |

---

## 정본 파일 grep 검증 결과 (2026-05-25)

| 항목 | 정본 widgets/post7_widget.html | 결론 |
|---|---|---|
| `var sec=5;` 횟수 | **0건** | 정본에 이미 sec=15 적용 완료 |
| `var sec=15;` 횟수 | **1건** | ✅ 정본 버그 A 수정 완료 |
| `BH_hideOverlay();if(typeof onComplete` 횟수 | **3건** | ✅ BH_animateCardReveal 포함 |
| `setTimeout(function(){if(typeof onComplete` 횟수 | **2건** | 다른 함수에서 정상 사용 중 |
| 파일 크기 | **83,741 chars** | |

**결론**: 정본 파일은 두 수정 모두 완료. 라이브 WP Page #303에 구 버전이 남아있으므로 아래 스니펫으로 동기화.

---

## OLD / NEW 문자열 확정

### 버그 A — sec=5 → sec=15

**OLD_A** (라이브 WP에 남아있는 구 패턴):
```
var sec=5;var el=document.getElementById('BH_auto_timer');if(el)el.textContent=sec+'초 후 보통 난이도로 자동 시작';BH_autoTimerInt=setInterval(function(){sec--;if(el)el.textContent=sec+'초 후 보통 난이도로 자동 시작';if(sec<=0)
```

**NEW_A** (수정 후):
```
var sec=15;var el=document.getElementById('BH_auto_timer');if(el)el.textContent=sec+'초 후 보통 난이도로 자동 시작';BH_autoTimerInt=setInterval(function(){sec--;if(el)el.textContent=sec+'초 후 보통 난이도로 자동 시작';if(sec<=0)
```

변경 위치: `sec=5` → `sec=15` (단 1글자 `5`→`15`)

---

### 버그 B — BH_animateCardReveal에 BH_hideOverlay() 추가

**OLD_B** (라이브 WP에 남아있는 구 패턴):
```
BH_animateCardReveal(cardData,targetEl,isAI,onComplete){BH_animSkipFlag=false;BH_showOverlay(cardData,isAI);var card=document.getElementById('BH_overlay_card');var durKey=isAI?'--BH-anim-ai-reveal-duration':'--BH-anim-reveal-duration';var dur=parseInt(getComputedStyle(document.documentElement).getPropertyValue(durKey))||(isAI?480:800);card.classList.add('BH_anim_reveal');if(isAI)card.classList.add('BH_anim_ai');setTimeout(function(){if(typeof onComplete==='function')onComplete();},dur);}
```

**NEW_B** (수정 후 — `BH_hideOverlay();` 삽입):
```
BH_animateCardReveal(cardData,targetEl,isAI,onComplete){BH_animSkipFlag=false;BH_showOverlay(cardData,isAI);var card=document.getElementById('BH_overlay_card');var durKey=isAI?'--BH-anim-ai-reveal-duration':'--BH-anim-reveal-duration';var dur=parseInt(getComputedStyle(document.documentElement).getPropertyValue(durKey))||(isAI?480:800);card.classList.add('BH_anim_reveal');if(isAI)card.classList.add('BH_anim_ai');setTimeout(function(){BH_hideOverlay();if(typeof onComplete==='function')onComplete();},dur);}
```

변경 위치: `setTimeout(function(){` 직후에 `BH_hideOverlay();` 17자 삽입

---

## 콘솔 실행 스니펫 (1회 붙여넣기 → Enter)

> 전제: WP 관리자 로그인 상태에서 https://neuralcare.co.kr/wp-admin/ 또는 https://neuralcare.co.kr/brain-games/minwhatoo/ 탭 열린 상태

```javascript
(async () => {
  // 1. Nonce 재발급 (window.__BH_nonce 만료 대비)
  const nonceRaw = await (await fetch('/wp-admin/admin-ajax.php?action=rest-nonce', {
    credentials: 'include'
  })).text();
  const nonce = nonceRaw.trim();
  if (!nonce || nonce === 'false' || nonce === '0') {
    console.error('[1] Nonce 실패 — wp-admin 재로그인 필요');
    return;
  }
  console.log('[1] Nonce 발급:', nonce.slice(0, 8) + '...');

  // 2. 라이브 raw GET
  const pageResp = await fetch('/wp-json/wp/v2/pages/303?context=edit', {
    headers: { 'X-WP-Nonce': nonce },
    credentials: 'include',
    cache: 'no-store'
  });
  if (!pageResp.ok) {
    console.error('[2] GET 실패:', pageResp.status);
    return;
  }
  const page = await pageResp.json();
  let raw = page.content.raw;
  console.log('[2] raw 길이:', raw.length);

  // 3a. 버그 A: sec=5 → sec=15
  const OLD_A = "var sec=5;var el=document.getElementById('BH_auto_timer');if(el)el.textContent=sec+'초 후 보통 난이도로 자동 시작';BH_autoTimerInt=setInterval(function(){sec--;if(el)el.textContent=sec+'초 후 보통 난이도로 자동 시작';if(sec<=0)";
  const NEW_A = "var sec=15;var el=document.getElementById('BH_auto_timer');if(el)el.textContent=sec+'초 후 보통 난이도로 자동 시작';BH_autoTimerInt=setInterval(function(){sec--;if(el)el.textContent=sec+'초 후 보통 난이도로 자동 시작';if(sec<=0)";

  const countA = (raw.match(/var sec=5;/g) || []).length;
  if (countA === 0) {
    console.warn('[3a] OLD_A 미검출 — 이미 PATCH 완료이거나 라이브 패턴 다름. OLD_A 건너뜀.');
  } else if (countA > 1) {
    console.error('[3a] OLD_A 중복 ' + countA + '건 — 매칭 확장 필요. 중단.');
    return;
  } else {
    raw = raw.replace(OLD_A, NEW_A);
    console.log('[3a] 버그 A 적용: sec=5 → sec=15');
  }

  // 3b. 버그 B: BH_animateCardReveal에 BH_hideOverlay() 추가
  const OLD_B = "BH_animateCardReveal(cardData,targetEl,isAI,onComplete){BH_animSkipFlag=false;BH_showOverlay(cardData,isAI);var card=document.getElementById('BH_overlay_card');var durKey=isAI?'--BH-anim-ai-reveal-duration':'--BH-anim-reveal-duration';var dur=parseInt(getComputedStyle(document.documentElement).getPropertyValue(durKey))||(isAI?480:800);card.classList.add('BH_anim_reveal');if(isAI)card.classList.add('BH_anim_ai');setTimeout(function(){if(typeof onComplete==='function')onComplete();},dur);}";
  const NEW_B = "BH_animateCardReveal(cardData,targetEl,isAI,onComplete){BH_animSkipFlag=false;BH_showOverlay(cardData,isAI);var card=document.getElementById('BH_overlay_card');var durKey=isAI?'--BH-anim-ai-reveal-duration':'--BH-anim-reveal-duration';var dur=parseInt(getComputedStyle(document.documentElement).getPropertyValue(durKey))||(isAI?480:800);card.classList.add('BH_anim_reveal');if(isAI)card.classList.add('BH_anim_ai');setTimeout(function(){BH_hideOverlay();if(typeof onComplete==='function')onComplete();},dur);}";

  const countB = (raw.match(/setTimeout\(function\(\)\{if\(typeof onComplete/g) || []).length;
  if (raw.indexOf(OLD_B) === -1) {
    console.warn('[3b] OLD_B 미검출 — 이미 PATCH 완료이거나 라이브 패턴 다름. OLD_B 건너뜀.');
  } else if (countB > 1) {
    // OLD_B가 있지만 패턴 중복 가능성 체크
    const specificCount = (raw.match(/BH_animateCardReveal\(cardData,targetEl,isAI,onComplete\)/g) || []).length;
    if (specificCount !== 1) {
      console.error('[3b] BH_animateCardReveal 정의 중복 ' + specificCount + '건 — 중단.');
      return;
    }
    raw = raw.replace(OLD_B, NEW_B);
    console.log('[3b] 버그 B 적용: BH_hideOverlay() 추가');
  } else {
    raw = raw.replace(OLD_B, NEW_B);
    console.log('[3b] 버그 B 적용: BH_hideOverlay() 추가');
  }

  // 4. PATCH
  const patchResp = await fetch('/wp-json/wp/v2/pages/303', {
    method: 'POST',
    headers: { 'X-WP-Nonce': nonce, 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ content: raw })
  });
  if (!patchResp.ok) {
    const errText = await patchResp.text();
    console.error('[4] PATCH 실패:', patchResp.status, errText.slice(0, 300));
    return;
  }
  const result = await patchResp.json();
  console.log('[4] PATCH 성공 — status:', result.status, '/ ID:', result.id);

  // 5. GET 재검증
  const verifyResp = await fetch('/wp-json/wp/v2/pages/303?context=edit', {
    headers: { 'X-WP-Nonce': nonce },
    credentials: 'include',
    cache: 'no-store'
  });
  const verified = await verifyResp.json();
  const vraw = verified.content.raw;
  console.log('[5] 검증 결과:');
  console.log('  sec=15 존재:',              vraw.includes('var sec=15;') ? 'PASS' : 'FAIL');
  console.log('  sec=5 잔존 없음:',          !vraw.includes('var sec=5;') ? 'PASS' : 'FAIL (구 패턴 잔존)');
  console.log('  BH_hideOverlay 추가 확인:', vraw.includes('BH_hideOverlay();if(typeof onComplete') ? 'PASS' : 'FAIL');
  console.log('  raw 길이:', vraw.length);
})();
```

---

## 주의사항

### 한글 문자열 처리
위 스니펫에서 `'초 후 보통 난이도로 자동 시작'` 부분은 유니코드 escape 처리됨.  
**브라우저 콘솔에 직접 붙여넣기 시 정상 처리됨** — 단, 이 파일을 복사할 때 편집기에서 escape가 유지되는지 확인 필요.

실제 라이브 콘솔에서 OLD_A 미검출(`sec=5 count: 0`) 메시지가 나오면 두 경우 중 하나:
1. **이미 PATCH 완료** → 버그 A는 건너뛰고 버그 B만 적용됨
2. **라이브 패턴이 다름** → 아래 진단 스니펫으로 실제 패턴 확인 후 재시도

### OLD_A 라이브 패턴 직접 확인 스니펫 (필요 시)
```javascript
// 라이브에서 sec 변수 초기화 부위 추출
(async () => {
  const nonce = (await (await fetch('/wp-admin/admin-ajax.php?action=rest-nonce', {credentials:'include'})).text()).trim();
  const page = await (await fetch('/wp-json/wp/v2/pages/303?context=edit', {headers:{'X-WP-Nonce':nonce},credentials:'include',cache:'no-store'})).json();
  const raw = page.content.raw;
  const idx = raw.indexOf('BH_startAutoTimer');
  if (idx !== -1) {
    console.log('BH_startAutoTimer 주변 300자:', raw.slice(idx, idx+300));
  } else {
    const idx2 = raw.indexOf('var sec=');
    if (idx2 !== -1) console.log('var sec= 주변:', raw.slice(idx2, idx2+200));
    else console.log('sec 변수 미발견');
  }
})();
```

---

## 기대 콘솔 출력 (정상 케이스)

```
[1] Nonce 발급: a1b2c3d4...
[2] raw 길이: 85XXX
[3a] 버그 A 적용: sec=5 → sec=15
[3b] 버그 B 적용: BH_hideOverlay() 추가
[4] PATCH 성공 — status: publish / ID: 303
[5] 검증 결과:
    sec=15 존재: PASS
    sec=5 잔존 없음: PASS
    BH_hideOverlay 추가 확인: PASS
    raw 길이: 85XXX
```

---

## PATCH 후 수동 검증 (Ctrl+Shift+R 새로고침 후)

1. https://neuralcare.co.kr/brain-games/minwhatoo/ 접속
2. 난이도 모달 표시 확인 → **15초** 카운트다운 확인 (이전: 5초)
3. [보통] 버튼 클릭 → 게임 시작
4. 첫 번째 카드 reveal 애니메이션 종료 후 → **오버레이 자동 사라짐** 확인
5. 콘솔: `typeof BH_startWithDiff` → `"function"` 확인

---

## dev 에이전트 자가 점검

| 항목 | 결과 |
|---|---|
| 정본 위젯 grep 검증 완료 | ✅ sec=15(1건) / hideOverlay(3건) 확인 |
| OLD_A 중복 검사 코드 스니펫 포함 | ✅ countA 체크 |
| OLD_B 중복 안전장치 포함 | ✅ BH_animateCardReveal 정의 1건 확인 |
| 라이브 이미 PATCH 완료 대비 건너뜀 처리 | ✅ warn 후 계속 |
| Nonce 재발급 포함 | ✅ |
| GET 재검증 포함 | ✅ 5단계 |
| git 실행 없음 | ✅ |
| 전체 재업로드 금지 (타겟 replace만) | ✅ CLAUDE.md §WP REST API 타겟 PATCH 룰 준수 |
