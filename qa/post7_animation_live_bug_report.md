# Post #7 민화투 라이브 버그 진단 보고서
**작성**: game 에이전트 v3.44 / 2026-05-25  
**대상 파일**: `C:\Claude_code\widgets\post7_widget.html` (85,025 bytes)  
**라이브 URL**: https://neuralcare.co.kr/brain-games/minwhatoo/ (WP Page ID: 303)

---

## 협업 약속 자가 점검

| # | 약속 | 결과 | 비고 |
|---|------|------|------|
| 1 | lead 지시 범위 준수 (진단 + 수정안 제시만) | ✅ | PATCH 스니펫 제공. 실제 git/WP 작업 없음 |
| 2 | 운영자 표기 룰 (neuralcare.co.kr) | ✅ | 하이픈 없음 유지 |
| 3 | YMYL 의료 단정 표현 0 | ✅ | |
| 4 | game.md + 정본 위젯 + design_ui + 기획서 사전 Read 완료 | ✅ | game.md, post7_widget.html, post7_animation_ui.html 정적 분석 완료 |
| 5 | 자기 단계 인지 (라이브 Critical 버그 디버깅) | ✅ | |
| 6 | 출력 형식 (박스·표·기호) | ✅ | |
| 7 | lead 단일 보고 | ✅ | |
| 8 | git 자의적 실행 0건 (보안 사고 재발 방지) | ✅ | git 명령 없음 |

---

## 1. 버그 A — 난이도 선택 모달 자동 진행 (Root Cause 확정)

### 증상
사용자가 [쉬움/보통/어려움] 버튼을 누르기 전에 게임이 자동 시작됨.

### 가설 검증 결과

| 가설 | 결과 | 근거 |
|---|---|---|
| A1: BH_initAnimSpeed에 자동 호출 코드 | ❌ 아님 | BH_initAnimSpeed = localStorage 복원 + CSS 변수 설정만. 게임 시작 없음 |
| A2: design_ui IIFE 형태로 모달 dismiss | ❌ 아님 | post7_animation_ui.html 분석 — IIFE 없음, 순수 CSS/HTML 블록 |
| A3: BH_auto_timer 카운트다운 너무 짧음 | ✅ **ROOT CAUSE** | sec=5 (5초). 시니어 UX 기준 위반. 상세 아래 |
| A4: BH_diff_modal style.display 누락 | ❌ 아님 | CSS .BH_difficulty_modal { display:flex } 있고 dm.style.display='' 정상 작동 |

### 근본 원인 상세

**코드 위치**: 정본 위젯 JS (단일행) 내 `BH_startAutoTimer` 함수 (pos 80052)

```
현재 코드:
var sec=5; ... BH_autoTimerInt=setInterval(...1000)
→ 5초 후 BH_startWithDiff('normal') 자동 호출
```

**문제 2**: `BH_showDifficultyModal`이 `DOMContentLoaded` 없이 IIFE 마지막에서 즉시 호출됨.  
WP iframe 로드 지연(최초 방문 시 1~3초)을 감안하면 실제 사용자에게 남은 시간은 **2~4초**.  
시니어 사용자(65세+)가 화면을 파악하고 버튼을 누르기에 절대적으로 부족함.

**game.md 위반 항목**: 시니어 UX 원칙 "60초+ 집중 요구 금지" / "느리고 크고 명확하게"

### 수정안

| 항목 | 현재 | 수정 |
|---|---|---|
| sec 초기값 | 5 | **15** (시니어 UX — 15초로 연장) |
| 카운트다운 텍스트 | 그대로 유지 | 그대로 유지 (ASCII 텍스트 — 깨짐 없음) |

---

## 2. 버그 B — 1월 광 카드 오버레이 안 사라짐 (Root Cause 확정)

### 증상
게임 시작 후 첫 번째 카드 reveal 애니메이션이 끝난 뒤 확대 오버레이가 화면에 그대로 남아 있음.

### 가설 검증 결과

| 가설 | 결과 | 근거 |
|---|---|---|
| B1: BH_hideOverlay() 호출 누락 | ✅ **ROOT CAUSE** | BH_animateCardReveal setTimeout 내부에 BH_hideOverlay 없음 |
| B2: animationend 이벤트 미등록 | ❌ 관련 없음 | setTimeout 방식 사용 — animationend 의존 없음 |
| B3: WP CSS 특이성 충돌 | ❌ 해당 없음 | .BH_overlay_card에 !important 적용. CSS 충돌 없음 |
| B4: onComplete 콜백 미전달 | ❌ 아님 | onComplete는 호출됨. 문제는 hideOverlay 누락 |
| B5: 가설 A의 연쇄 결과 | ✅ 부분 연관 | 자동 5초 진행 → 첫 턴에 즉시 카드 reveal → B 버그 노출 |

### 근본 원인 상세

**코드 위치**: 정본 위젯 JS, `BH_animateCardReveal` 함수 (pos 54055, 길이 492자)

**현재 코드** (핵심 부분):
```
BH_animateCardReveal(cardData,targetEl,isAI,onComplete){
  ...
  setTimeout(function(){
    if(typeof onComplete==='function')onComplete();  // ← BH_hideOverlay() 없음!
  }, dur);
}
```

**다른 animate 함수와 비교** (`BH_animatePlace`, `BH_animateDeckFlip` 등):
```
// BH_animatePlace (정상): setTimeout 안에 BH_hideOverlay() 있음 (pos 55981)
BH_hideOverlay();if(typeof onComplete==='function')onComplete();
```

`BH_animateCardReveal`만 유독 `BH_hideOverlay()` 호출이 빠진 구현 버그.

### 수정안

`BH_animateCardReveal`의 setTimeout 콜백에 `BH_hideOverlay()` 추가:

---

## 3. 수정 적용 전 콘솔 진단 스니펫

사용자가 라이브 https://neuralcare.co.kr/brain-games/minwhatoo/ 에서 브라우저 콘솔(F12)에 붙여넣기:

```javascript
// === 진단 스니펫 ===
// 1. 게임 함수 로드 확인
console.log('BH_startWithDiff:', typeof window.BH_startWithDiff);
console.log('BH_showDifficultyModal:', typeof window.BH_showDifficultyModal);
console.log('BH_animateCardReveal:', typeof window.BH_animateCardReveal);

// 2. 현재 모달/게임 상태
var dm = document.getElementById('BH_diff_modal');
var gb = document.getElementById('BH_game_board');
var oc = document.getElementById('BH_overlay_card');
console.log('diff_modal display:', dm ? dm.style.display : 'NOT FOUND');
console.log('game_board display:', gb ? gb.style.display : 'NOT FOUND');
console.log('overlay_card display:', oc ? oc.style.display : 'NOT FOUND');

// 3. BH_GS 상태 (게임 중일 때)
if (typeof window.BH_GS !== 'undefined') {
  console.log('BH_GS.phase:', BH_GS.phase);
  console.log('BH_GS.animStage:', BH_GS.animStage);
}

// 4. 오버레이 강제 hide (임시 조치)
if (oc) { oc.style.display = 'none'; console.log('overlay_card 강제 hide 완료'); }
var dim = document.getElementById('BH_overlay_dim');
if (dim) { dim.style.display = 'none'; console.log('overlay_dim 강제 hide 완료'); }
```

---

## 4. 타겟 PATCH 스니펫 (lead 검토 후 dev 에이전트 실행)

아래 두 수정을 **정본 파일에 직접 Edit** 후 → WP REST API 타겟 PATCH.

### 수정 1: 버그 A — auto_timer sec 값 변경

**old_string** (정본 위젯 JS 단일행 내):
```
var sec=5;var el=document.getElementById('BH_auto_timer');if(el)el.textContent=sec+'초 후 보통 난이도로 자동 시작';BH_autoTimerInt=setInterval(function(){sec--;if(el)el.textContent=sec+'초 후 보통 난이도로 자동 시작';if(sec<=0)
```

**new_string**:
```
var sec=15;var el=document.getElementById('BH_auto_timer');if(el)el.textContent=sec+'초 후 보통 난이도로 자동 시작';BH_autoTimerInt=setInterval(function(){sec--;if(el)el.textContent=sec+'초 후 보통 난이도로 자동 시작';if(sec<=0)
```

### 수정 2: 버그 B — BH_animateCardReveal hideOverlay 추가

**old_string** (정본 위젯 JS 단일행 내, pos 54055):
```
BH_animateCardReveal(cardData,targetEl,isAI,onComplete){BH_animSkipFlag=false;BH_showOverlay(cardData,isAI);var card=document.getElementById('BH_overlay_card');var durKey=isAI?'--BH-anim-ai-reveal-duration':'--BH-anim-reveal-duration';var dur=parseInt(getComputedStyle(document.documentElement).getPropertyValue(durKey))||(isAI?480:800);card.classList.add('BH_anim_reveal');if(isAI)card.classList.add('BH_anim_ai');setTimeout(function(){if(typeof onComplete==='function')onComplete();},dur);}
```

**new_string** (`BH_hideOverlay()` 추가):
```
BH_animateCardReveal(cardData,targetEl,isAI,onComplete){BH_animSkipFlag=false;BH_showOverlay(cardData,isAI);var card=document.getElementById('BH_overlay_card');var durKey=isAI?'--BH-anim-ai-reveal-duration':'--BH-anim-reveal-duration';var dur=parseInt(getComputedStyle(document.documentElement).getPropertyValue(durKey))||(isAI?480:800);card.classList.add('BH_anim_reveal');if(isAI)card.classList.add('BH_anim_ai');setTimeout(function(){BH_hideOverlay();if(typeof onComplete==='function')onComplete();},dur);}
```

---

## 5. WP 라이브 PATCH 절차 (dev 에이전트 실행)

```
1. GET /wp-json/wp/v2/pages/303?context=edit → raw content 취득
2. rawContent.replace(old_string_A, new_string_A) → 버그 A 수정
3. rawContent.replace(old_string_B, new_string_B) → 버그 B 수정
4. replace 후 검증:
   - indexOf('var sec=5') === -1  ← 구문자 소멸 확인
   - indexOf('var sec=15') !== -1  ← 신문자 존재 확인
   - indexOf('BH_hideOverlay();if(typeof onComplete') !== -1  ← B 수정 확인
5. PATCH /wp-json/wp/v2/pages/303 with 수정된 raw content
6. GET 재확인 + typeof BH_startWithDiff 콘솔 검증
```

---

## 6. 요약

| 버그 | Root Cause | 심각도 | 수정 크기 |
|---|---|---|---|
| A. 난이도 모달 자동 진행 | BH_startAutoTimer sec=5 (5초) — 시니어 조작 불가 | Critical | sec=5 → sec=15 (1글자) |
| B. 오버레이 미해제 | BH_animateCardReveal setTimeout에 BH_hideOverlay() 누락 | Critical | BH_hideOverlay(); 추가 (17자) |

두 수정 모두 **단일 문자열 replace** 수준 — 전체 위젯 재업로드 불필요. 타겟 PATCH 적용 가능.
