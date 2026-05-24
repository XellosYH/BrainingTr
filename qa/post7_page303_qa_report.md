# QA 리포트 — post7 / Page 303 (민화투 허브 페이지)

**작성**: QA 에이전트 v8.56  
**일시**: 2026-05-22  
**대상 파일**: `C:\Claude_code\widgets\post7_widget_v2.html`  
**대상 페이지**: https://neuralcare.co.kr/brain-games/minwhatoo/ (WP Page ID: 303)  
**파이프라인**: 게임 전용 허브 페이지 검수 (qa.md § 게임 전용 검수 파이프라인)

---

## 1. SW 검증 결과 (4개 함수별 현황)

| 함수명 | typeof 결과 | 판정 |
|---|---|---|
| `BH_startWithDiff` | `"function"` | ✅ PASS |
| `BH_restartGame` | `"undefined"` | ❌ FAIL |
| `BH_confirmNewGame` | `"undefined"` | ❌ FAIL |
| `BH_startAutoTimer` | `"undefined"` | ❌ FAIL |

**추가 발견 (HTML onclick 호출 함수 전수 조사)**:

| 함수명 | window 노출 | 전역 접근 가능 여부 |
|---|---|---|
| `BH_startWithDiff` | ✅ `window.BH_startWithDiff=function...` | ✅ 가능 |
| `BH_toggleMute` | ✅ `window.BH_toggleMute=function...` | ✅ 가능 |
| `BH_shareResult` | ✅ `window.BH_shareResult=function...` | ✅ 가능 |
| `BH_restartGame` | ❌ 없음 | ❌ 불가 (`undefined`) |
| `BH_confirmNewGame` | ❌ 없음 | ❌ 불가 (`undefined`) |
| `BH_startAutoTimer` | ❌ 없음 | ❌ 불가 (`undefined`) |
| `BH_showHint` | ❌ 없음 | ❌ 불가 (`undefined`) |
| `BH_toggleHow` | ❌ 없음 | ❌ 불가 (`undefined`) |

**SW 검수 결론**: ❌ FAIL — 총 5개 함수가 전역 미노출 상태

---

## 2. undefined 원인 분석

### 근본 원인: IIFE 내부 function 선언 vs window 할당 불일치

전체 `<script>` 블록이 IIFE(즉시 실행 함수 표현식)로 감싸져 있다:

```js
(function(){
  // ... 모든 코드 ...
}());
```

IIFE 내부에서 `function BH_xxx()` 형태로 선언된 함수는 **IIFE 스코프에 갇혀** 전역(`window`)에서 접근 불가하다.

### 전역 노출된 함수 (올바른 패턴 — 참고용):
```js
window.BH_startWithDiff = function(diff){ ... };
window.BH_toggleMute = function(){ ... };
window.BH_shareResult = function(){ ... };
```

### 전역 미노출 함수 (잘못된 패턴 — 수정 필요):
```js
// IIFE 내부에만 있음 — window에서 접근 불가
function BH_restartGame(){ ... }         // 전역 노출 누락
function BH_confirmNewGame(){ ... }      // 전역 노출 누락
function BH_startAutoTimer(){ ... }      // 전역 노출 누락
function BH_showHint(){ ... }            // 전역 노출 누락 (추가 발견)
function BH_toggleHow(){ ... }           // 전역 노출 누락 (추가 발견)
```

### HTML onclick 충돌:
HTML의 `onclick="BH_confirmNewGame()"` 등은 **전역 스코프**에서 함수를 찾는다. IIFE 내부 function 선언은 전역에서 찾을 수 없으므로 `ReferenceError` 또는 `undefined` 결과가 나온다.

**증거**: `BH_startWithDiff`는 IIFE 내부에서 `window.BH_startWithDiff = function(...)` 으로 명시적 할당이 되어 있어 `typeof === "function"` 결과가 나온다. 나머지 3개(+2개)는 이 패턴이 없다.

---

## 3. game 에이전트 수정 필요 사항

### 수정 파일: `C:\Claude_code\widgets\post7_widget_v2.html`

### 수정 방법 (2가지 중 선택):

**방법 A (권장): `window.` 할당 방식으로 전환**

IIFE 내부에서 각 함수를 window에 할당:

```js
// 변경 전 (IIFE 내부)
function BH_restartGame(){ ... }
function BH_confirmNewGame(){ ... }
function BH_startAutoTimer(){ ... }
function BH_showHint(){ ... }
function BH_toggleHow(){ ... }

// 변경 후
window.BH_restartGame = function(){ ... };
window.BH_confirmNewGame = function(){ ... };
window.BH_startAutoTimer = function(){ ... };
window.BH_showHint = function(){ ... };
window.BH_toggleHow = function(){ ... };
```

**방법 B: IIFE 끝에서 window 일괄 할당**

IIFE 마지막 `}());` 직전에 추가:

```js
window.BH_restartGame = BH_restartGame;
window.BH_confirmNewGame = BH_confirmNewGame;
window.BH_startAutoTimer = BH_startAutoTimer;
window.BH_showHint = BH_showHint;
window.BH_toggleHow = BH_toggleHow;
```

### 수정 후 재검증 필수:
```js
typeof BH_startWithDiff === "function"   // ✅ 이미 PASS
typeof BH_restartGame === "function"     // 수정 후 확인 필요
typeof BH_confirmNewGame === "function"  // 수정 후 확인 필요
typeof BH_startAutoTimer === "function"  // 수정 후 확인 필요
typeof BH_showHint === "function"        // 수정 후 확인 필요
typeof BH_toggleHow === "function"       // 수정 후 확인 필요
```

---

## 4. S3 결과 (한글 Mojibake)

| 패턴 | 검출 건수 | 판정 |
|---|---|---|
| `ë` (Latin-1 한글 오염) | 0건 | ✅ PASS |
| `ì` (Latin-1 한글 오염) | 0건 | ✅ PASS |
| `í` (Latin-1 한글 오염) | 0건 | ✅ PASS |
| `ê¸` (Latin-1 한글 오염) | 0건 | ✅ PASS |
| `â€` (UTF-8 오염) | 0건 | ✅ PASS |
| `Ã` (Latin-1 오염) | 0건 | ✅ PASS |

**S3 결론**: ✅ PASS — Mojibake 0건

---

## 5. 도박 금지어 체크

| 금지어 | 검출 건수 | 판정 |
|---|---|---|
| 배팅 | 0건 | ✅ PASS |
| 판돈 | 0건 | ✅ PASS |
| 도박 | 0건 | ✅ PASS |
| 사행 | 0건 | ✅ PASS |
| 카지노 | 0건 | ✅ PASS |
| 베팅 | 0건 | ✅ PASS |
| 베트 | 0건 | ✅ PASS |

**도박 금지어 결론**: ✅ PASS — 0건

---

## 6. 추가 검증 결과

### JS 내 이모지 (WP wp_staticize_emoji 위험)
- JS `<script>` 블록 내 이모지: **0건** ✅ PASS
- HTML 영역 이모지(버튼 텍스트 등): 정상 (JS 밖이므로 문제 없음)

### 면책 문구
- `"참고용 두뇌훈련 게임 · 의료적 진단이 아닙니다"`: **1건 존재** ✅ PASS

### window에 노출된 BH_ 함수/변수 현황 (현재 상태)
총 14개: `BH_AudioContext`, `BH_playClick`, `BH_playWrong`, `BH_playCardPlace`, `BH_playCardMatch`, `BH_playComplete`, `BH_playFanfare`, `BH_playReset`, `BH_playJokboSound`, `BH_toggleMute`, `BH_SoundMuted`, `BH_startWithDiff`, `BH_shareResult`, `BH_showDifficultyModal`

---

## 7. 종합 판정

| 항목 | 판정 |
|---|---|
| SW (BH_startWithDiff) | ✅ PASS |
| SW (BH_restartGame) | ❌ FAIL |
| SW (BH_confirmNewGame) | ❌ FAIL |
| SW (BH_startAutoTimer) | ❌ FAIL |
| SW 추가 발견 (BH_showHint) | ❌ FAIL |
| SW 추가 발견 (BH_toggleHow) | ❌ FAIL |
| S3 (Mojibake) | ✅ PASS |
| 도박 금지어 | ✅ PASS |
| 면책 문구 | ✅ PASS |
| JS 이모지 | ✅ PASS |

**전체 판정**: ❌ SW FAIL — game 에이전트 수정 후 재검수 필요

---

## 8. game 에이전트 지시 요약

**수정 파일**: `C:\Claude_code\widgets\post7_widget_v2.html`  
**수정 우선도**: CRITICAL — onclick 버튼 5개가 동작 불가 상태

**수정 내용**:
1. IIFE 내에서 `function BH_restartGame()`을 `window.BH_restartGame = function()` 형태로 변경 (또는 IIFE 끝에서 window 할당)
2. 동일하게 `BH_confirmNewGame`, `BH_startAutoTimer`, `BH_showHint`, `BH_toggleHow` 5개 함수 모두 전역 노출 처리
3. Python minify 후 WP 재업로드
4. Chrome MCP로 `typeof BH_confirmNewGame === "function"` 등 6개 함수 전부 PASS 확인
5. 실제 버튼 클릭 동작 (재시작·힌트·방법 보기) 확인

**수정 후 QA 재호출 필수**
