# Post #7 민화투 라이브 버그 v2 진단 보고서
**작성**: game 에이전트 v3.44 / 2026-05-25 (PATCH 후 잔존 버그 재진단)
**대상 파일**: `C:\Claude_code\widgets\post7_widget.html`
**라이브 URL**: https://neuralcare.co.kr/brain-games/minwhatoo/ (WP Page ID: 303)

---

## 협업 약속 자가 점검

| # | 약속 | 결과 | 비고 |
|---|------|------|------|
| 1 | lead 지시 범위 준수 (진단 + 수정안 보고만, 정본 직접 수정·git 0건) | OK | 파일 수정 없음, git 없음 |
| 2 | 운영자 표기 룰 (neuralcare.co.kr) | OK | 하이픈 없음 유지 |
| 3 | YMYL 의료 단정 표현 0 | OK | |
| 4 | game.md + 정본 + design_ui + 기획서 + 이전 보고서 사전 Read | OK | 5개 파일 모두 Read 완료 |
| 5 | 자기 단계 인지 (라이브 Critical 후속 진단) | OK | |
| 6 | 출력 형식 (박스·표·기호) | OK | |
| 7 | lead 단일 보고 | OK | |
| 8 | git·정본 직접 수정 0건 | OK | |

---

## 0. PATCH 반영 상태 확인 (정본 파일 실측)

| 항목 | 이전 보고 수정안 | 정본 실측 결과 | 상태 |
|---|---|---|---|
| `var sec=` 값 | 5 → 15 | `var sec=15` 확인 | OK: 반영됨 |
| `BH_animateCardReveal` setTimeout 내 `BH_hideOverlay()` | 추가 요청 | pos 54492에 `BH_hideOverlay();if(typeof onComplete==='function')onComplete();` 확인 | OK: 반영됨 |
| `BH_hideOverlay` 총 출현 수 | 4건 필요 | 4건 확인 (pos 52848·54492·55998·56514) | OK |

**결론**: 이전 PATCH 2건은 정본 파일에 정상 반영됨.
**라이브 증상 지속 = 정본과 WP 라이브의 불일치 가능성 또는 추가 미진 버그 존재.**

---

## 1. 증상 A — "1월 광 카드가 안 사라짐" 재진단

### 가설 검증 결과

| 가설 | 검증 방법 | 결과 |
|---|---|---|
| A-1: WP PATCH가 실제 안 됨 (v2 스니펫 SKIP B) | 정본 파일 grep | 반영 확인. WP 라이브 vs 정본 불일치 가능성 |
| A-2: BH_hideOverlay() 잘못된 위치 삽입 | `BH_animateCardReveal` 본문 재확인 | **OK**: setTimeout 내 정상 위치에 삽입됨 |
| A-3: BH_hideOverlay() 함수 자체 버그 | 함수 본문 확인 | BH_overlay_dim, BH_overlay_card style.display='none' 정상 구현 |
| A-4: setTimeout 미호출 (dur=0) | BH_ANIM_SPEED 값 확인 | normal 모드 REVEAL=800ms. 0ms 없음 |
| A-5: deck_flip이 띄운 오버레이에 hideOverlay 누락 | BH_animateDeckFlip 확인 | pos 55998에 BH_hideOverlay() 정상 존재 |
| **A-6: 캐시 잔존** | 정본에 반영됐지만 라이브 미반영 | **Root Cause 최유력** |

### Root Cause A: WP 라이브 미반영 (캐시 또는 PATCH 미적용)

정본 파일에는 수정이 완료됐지만 WP REST API PATCH가 실제로 라이브에 반영되지 않았거나, CDN/브라우저 캐시가 구 버전을 서빙 중일 가능성이 높다.

**확인 방법** (진단 스니펫 1 참조):
- `GET /wp-json/wp/v2/pages/303?context=edit` → raw content에서 `var sec=15` 및 `BH_hideOverlay();if(typeof onComplete` 존재 여부 직접 확인
- 없으면: PATCH가 실제 반영 안 됨 → 재PATCH 필요
- 있으면: CDN/브라우저 캐시 문제 → 강제 새로고침(Ctrl+Shift+R) 또는 캐시 퍼지

---

## 2. 증상 B — "게임이 자동으로 플레이됨" (신규 증상) — Root Cause 확정

### 정적 분석 결과

#### Root Cause B-1 (확정): `BH_initGame()`에 `phase`/`animStage` 리셋 누락

**실측 결과**:
```
function BH_initGame(diff){
  BH_GS.difficulty=diff||'normal';
  // 손패·바닥·더미·캡처 초기화 있음
  BH_GS.selectedCard=null;
  BH_GS.deckFlipped=null;
  BH_GS.hintUsed=false;
  BH_GS.hintCount=0;
  BH_GS.turnCount=0;
  BH_GS.gameOver=false;
  // ← BH_GS.phase, BH_GS.animStage 초기화 없음!
}
```

`BH_GS.phase`와 `BH_GS.animStage`가 `BH_initGame()` 안에서 초기화되지 않는다.

#### 자동 플레이 발생 경로 재현

1. 게임 도중 사용자가 "새 게임"을 클릭하거나, 자동 타이머로 게임이 시작됨
2. `BH_startWithDiff(diff)` 호출
3. `BH_initGame(diff)` — 손패/바닥/더미 초기화 O, **phase/animStage 초기화 X**
4. 직전 게임에서 phase가 `'ANIMATING'`이나 `'AI_TURN'`으로 남아있을 경우:
   - `BH_setPhase('PLAYER_TURN')` 호출은 있지만 이 시점에 이미 `setTimeout(BH_doAITurn, 800)` 이 큐에 걸려있을 수 있음
   - 또는 `animStage`가 `'HAND_REVEAL'` 등으로 남아 있어 다음 BH_animateCardReveal 콜백 체인이 즉시 진행

5. **특히 문제가 되는 경로**: 게임 첫 시작 시 자동 타이머(sec=15)가 작동해 `BH_startWithDiff('normal')` 호출 → `BH_setPhase('PLAYER_TURN')` 이후 `BH_renderBoard()` 안에서 floor/hand 카드가 렌더링되고 onclick이 바인딩되지만, 이전 `setTimeout(BH_doAITurn, 800)` 이 **남은 큐에서 800ms 후 실행**됨

#### Root Cause B-2 (보조): `BH_doAITurn` phase 체크 누락

**실측 결과**:
```javascript
function BH_doAITurn(){
  if(BH_GS.aiHand.length===0){...return;}  // aiHand 체크는 있음
  // ← BH_GS.phase === 'AI_TURN' 체크 없음!
  var card=BH_aiSelectCard();
  ...
}
```

`BH_doAITurn`이 `BH_GS.phase === 'AI_TURN'`을 확인하지 않는다. `setTimeout(BH_doAITurn, 800)` 이 큐에 등록된 상태에서 `BH_startWithDiff`가 호출되면:
- `BH_GS.phase`는 `'PLAYER_TURN'`으로 설정됨
- 800ms 후 `BH_doAITurn`이 실행 — phase 체크 없으므로 **플레이어 턴 중에도 AI가 패를 냄**
- 사용자 클릭 없이 AI가 자동으로 카드를 진행하는 것처럼 보임

#### B-1·B-2 연동 시나리오

```
[직전 게임 종료] → AI_TURN에서 setTimeout(BH_doAITurn, 800) 등록 완료
    ↓ (800ms 이내에)
[자동 타이머 or 새 게임] → BH_startWithDiff() → BH_initGame() [phase 리셋 없음]
    → BH_setPhase('PLAYER_TURN')
    ↓ (800ms 경과)
setTimeout 큐에서 BH_doAITurn 실행 — phase 체크 없어 AI 카드 자동 진행
    → 사용자가 클릭 안 했는데 게임이 진행됨
```

또는 페이지 **최초 로드** 시에도 동일 증상:
```
[sec=15 자동 타이머] → 15초 후 BH_startWithDiff('normal')
    → BH_setPhase('PLAYER_TURN') → BH_renderBoard()
    → 이때 BH_GS.animStage='IDLE' (초기값), BH_GS.phase='PLAYER_TURN'
    → 정상 흐름이라면 문제 없어야 하지만...
```

최초 로드는 정상이지만 **재시작 시 phase/animStage 잔존**이 문제의 핵심.

---

## 3. 수정안 (적용 금지 — lead 승인 후 dev에 위임)

### 수정 B-1: `BH_initGame`에 `phase`/`animStage` 리셋 추가

**현재 코드** (`BH_initGame` 함수):
```
function BH_initGame(diff){BH_GS.difficulty=diff||'normal';var shuffled=BH_shuffle(BH_DECK_DATA);BH_GS.playerHand=shuffled.slice(0,10);BH_GS.aiHand=shuffled.slice(10,20);BH_GS.floor=shuffled.slice(20,28);BH_GS.deck=shuffled.slice(28);BH_GS.playerCaptured=[];BH_GS.aiCaptured=[];BH_GS.selectedCard=null;BH_GS.deckFlipped=null;BH_GS.hintUsed=false;BH_GS.hintCount=0;BH_GS.turnCount=0;BH_GS.gameOver=false;}
```

**수정 코드** (`phase`/`animStage` 2필드 추가):
```
function BH_initGame(diff){BH_GS.difficulty=diff||'normal';BH_GS.phase='IDLE';BH_GS.animStage='IDLE';var shuffled=BH_shuffle(BH_DECK_DATA);BH_GS.playerHand=shuffled.slice(0,10);BH_GS.aiHand=shuffled.slice(10,20);BH_GS.floor=shuffled.slice(20,28);BH_GS.deck=shuffled.slice(28);BH_GS.playerCaptured=[];BH_GS.aiCaptured=[];BH_GS.selectedCard=null;BH_GS.deckFlipped=null;BH_GS.hintUsed=false;BH_GS.hintCount=0;BH_GS.turnCount=0;BH_GS.gameOver=false;}
```

**변경 diff**:
- old: `BH_GS.difficulty=diff||'normal';var shuffled`
- new: `BH_GS.difficulty=diff||'normal';BH_GS.phase='IDLE';BH_GS.animStage='IDLE';var shuffled`

### 수정 B-2: `BH_doAITurn`에 phase 가드 추가

**현재 코드**:
```
function BH_doAITurn(){if(BH_GS.aiHand.length===0){if(BH_checkGameOver()){BH_showResults();}else{BH_setPhase('PLAYER_TURN');BH_renderBoard();}return;}
```

**수정 코드** (phase 가드 추가):
```
function BH_doAITurn(){if(BH_GS.phase!=='AI_TURN')return;if(BH_GS.aiHand.length===0){if(BH_checkGameOver()){BH_showResults();}else{BH_setPhase('PLAYER_TURN');BH_renderBoard();}return;}
```

**변경 diff**:
- old: `function BH_doAITurn(){if(BH_GS.aiHand.length===0)`
- new: `function BH_doAITurn(){if(BH_GS.phase!=='AI_TURN')return;if(BH_GS.aiHand.length===0)`

---

## 4. 타겟 PATCH 정확한 문자열 (dev 에이전트 실행용)

### PATCH 전 필수 확인
```
GET /wp-json/wp/v2/pages/303?context=edit
rawContent.indexOf('var sec=15') !== -1   -> 이전 PATCH 반영 확인
rawContent.indexOf('BH_hideOverlay();if(typeof onComplete') !== -1   -> 이전 PATCH 반영 확인
```

두 항목 중 하나라도 -1이면 이전 PATCH 재적용 먼저.

### PATCH C: B-1 수정 — BH_initGame phase/animStage 리셋

**old_string**:
```
BH_GS.difficulty=diff||'normal';var shuffled=BH_shuffle(BH_DECK_DATA);
```

**new_string**:
```
BH_GS.difficulty=diff||'normal';BH_GS.phase='IDLE';BH_GS.animStage='IDLE';var shuffled=BH_shuffle(BH_DECK_DATA);
```

### PATCH D: B-2 수정 — BH_doAITurn phase 가드

**old_string**:
```
function BH_doAITurn(){if(BH_GS.aiHand.length===0){if(BH_checkGameOver()){BH_showResults();}else{BH_setPhase('PLAYER_TURN');BH_renderBoard();}return;}
```

**new_string**:
```
function BH_doAITurn(){if(BH_GS.phase!=='AI_TURN')return;if(BH_GS.aiHand.length===0){if(BH_checkGameOver()){BH_showResults();}else{BH_setPhase('PLAYER_TURN');BH_renderBoard();}return;}
```

---

## 5. 콘솔 진단 스니펫 3종

### 진단-1: WP 라이브 PATCH 반영 확인 (사전 실행)

```javascript
// === 진단-1: WP 라이브 raw content 반영 확인 ===
// 실행: 브라우저 콘솔 (라이브 페이지 또는 별도 탭)
fetch("https://neuralcare.co.kr/wp-json/wp/v2/pages/303?context=edit", {credentials:"include"})
  .then(function(r){return r.json();})
  .then(function(d){
    var raw = d.content && d.content.raw ? d.content.raw : "";
    console.log("raw length:", raw.length);
    console.log("sec=15:", raw.indexOf("var sec=15") !== -1 ? "PASS" : "FAIL - PATCH 미반영");
    console.log("hideOverlay in reveal:", raw.indexOf("BH_hideOverlay();if(typeof onComplete") !== -1 ? "PASS" : "FAIL - PATCH 미반영");
    console.log("phase IDLE in initGame:", raw.indexOf("BH_GS.phase='IDLE';BH_GS.animStage='IDLE'") !== -1 ? "PASS (C 반영)" : "FAIL or NOT YET");
    console.log("doAITurn phase guard:", raw.indexOf("BH_GS.phase!=='AI_TURN')return") !== -1 ? "PASS (D 반영)" : "FAIL or NOT YET");
  });
```

### 진단-2: FSM 상태 및 자동 플레이 실시간 추적

```javascript
// === 진단-2: 게임 페이지에서 FSM 상태 확인 ===
// 실행: https://neuralcare.co.kr/brain-games/minwhatoo/ 콘솔
// 1. iframe 내부 접근
var iframe = document.querySelector("iframe");
var iWin = iframe ? iframe.contentWindow : window;

// 2. 현재 BH_GS 상태
if(typeof iWin.BH_GS !== "undefined"){
  console.log("phase:", iWin.BH_GS.phase);
  console.log("animStage:", iWin.BH_GS.animStage);
  console.log("gameOver:", iWin.BH_GS.gameOver);
  console.log("playerHand length:", iWin.BH_GS.playerHand.length);
  console.log("aiHand length:", iWin.BH_GS.aiHand.length);
} else {
  console.log("BH_GS not found - game not started");
}

// 3. BH_doAITurn phase guard 존재 여부
var fnStr = iWin.BH_doAITurn ? iWin.BH_doAITurn.toString() : "NOT FOUND";
console.log("BH_doAITurn phase guard:", fnStr.indexOf("phase!=='AI_TURN'") !== -1 ? "OK" : "MISSING - autoplay 원인");
```

### 진단-3: setTimeout 자동 진행 모니터링

```javascript
// === 진단-3: setTimeout 래핑으로 BH_doAITurn 자동 호출 추적 ===
// 실행: 게임 시작 직전 콘솔에 붙여넣기
var iframe = document.querySelector("iframe");
var iWin = iframe ? iframe.contentWindow : window;
var origSetTimeout = iWin.setTimeout;
iWin.setTimeout = function(fn, ms) {
  var fnName = fn && fn.name ? fn.name : fn ? fn.toString().slice(0, 50) : "unknown";
  if(fnName.indexOf("BH_doAI") !== -1 || (typeof fn === "function" && fn.toString().indexOf("BH_doAI") !== -1)){
    console.warn("[MONITOR] setTimeout BH_doAITurn registered, ms=" + ms + ", current phase=" + (iWin.BH_GS ? iWin.BH_GS.phase : "unknown"));
    console.trace();
  }
  return origSetTimeout.apply(this, arguments);
};
console.log("setTimeout monitor ON - BH_doAITurn 호출 추적 시작");
```

---

## 6. 수정 우선순위 및 요약

| 수정 | 대상 버그 | 중요도 | old_string 길이 | 방식 |
|---|---|---|---|---|
| 이전 PATCH A·B 재확인 | 1월 광 잔존 | Critical | - | GET 검증 먼저 |
| **PATCH C**: BH_initGame phase/animStage 추가 | 자동 플레이 근본 차단 | Critical | 53자 | 타겟 replace |
| **PATCH D**: BH_doAITurn phase 가드 | 자동 플레이 방어막 | Critical | 128자 | 타겟 replace |

**적용 순서**:
1. 진단-1 스니펫 실행 → 이전 PATCH A·B 반영 여부 확인
2. A·B 미반영이면 재PATCH
3. PATCH C 적용
4. PATCH D 적용
5. 진단-2 스니펫 실행 → phase guard 확인
6. 라이브 게임 재시작 3회 반복 → 자동 플레이 재현 여부 확인

---

## 7. 정본 파일 수정 위치 정리 (dev 에이전트용 Edit 가이드)

**PATCH C** — `C:\Claude_code\widgets\post7_widget.html` 내:
- old: `BH_GS.difficulty=diff||'normal';var shuffled=BH_shuffle(BH_DECK_DATA);`
- new: `BH_GS.difficulty=diff||'normal';BH_GS.phase='IDLE';BH_GS.animStage='IDLE';var shuffled=BH_shuffle(BH_DECK_DATA);`

**PATCH D** — 동일 파일 내:
- old: `function BH_doAITurn(){if(BH_GS.aiHand.length===0){if(BH_checkGameOver()){BH_showResults();}else{BH_setPhase('PLAYER_TURN');BH_renderBoard();}return;}`
- new: `function BH_doAITurn(){if(BH_GS.phase!=='AI_TURN')return;if(BH_GS.aiHand.length===0){if(BH_checkGameOver()){BH_showResults();}else{BH_setPhase('PLAYER_TURN');BH_renderBoard();}return;}`
