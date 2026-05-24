# 화투 카드 인식 명확화 애니메이션 기획서
# Post #7 민화투 — 패 인식 개선 (v1.0)

**작성일**: 2026-05-25
**작성자**: game_planner 에이전트 v1.9
**대상 위젯**: `C:\Claude_code\widgets\post7_widget.html` (63,912 bytes)
**연계 태그**: `plan/p7-card-anim-v1.0`

---

## 협업 약속 자가 점검

| # | 약속 | 결과 | 비고 |
|---|------|------|------|
| 1 | lead 지시 범위 준수 | OK | 애니메이션 기획 범위만 작성 |
| 2 | 운영자 표기 룰 | OK | neuralcare.co.kr 표기 준수 |
| 3 | YMYL 의료 단정 표현 0 | OK | "두뇌 트레이닝" 언어만 사용 |
| 4 | game_planner.md Read 완료 | OK | 세션 시작 시 Read 완료 |
| 5 | 자기 단계 인지 (기획 단계) | OK | 구현 명세 아님, 기획 명세 |
| 6 | 출력 형식 (표/섹션 구조) | OK | 표·다이어그램·의사코드 포함 |
| 7 | lead 단일 보고 | OK | 기획서 완료 후 lead에 보고 |
| 8 | 18px+ UX (시니어 가독성) | OK | CSS 명세에 18px+ 최소치 명시 |

---

## 1. 요구사항 정리

### 사용자 원문 요구사항

> 내가 새로 뒤집는 패, 상대가 새로 낸 패, 상대가 새로 뒤집은 패가 잘 구분이 되지 않음.
> 새로 내거나 뒤집는 패는 한번 확대해서 이용자에게 보여준 후 바닥에 깔리도록 하는 애니메이션 효과가 필요함.
>
> 1. 내가 새로 뒤집은 패를 확대해서 보여주고
> 2. 뒤집은 패가 바닥에 깔린 패와 매치될 경우, 매치되는 패 옆에 살짝 겹쳤다가
> 3. 내가 획득한 패로 이동되도록
>
> 3단계를 천천히 진행해서 사용자가 충분히 패를 인식할 수 있도록 진행할 것

### 정체성 원칙 (필수)

이 게임은 도박이 아닙니다. 시니어 두뇌 트레이닝·인지 강화 도구입니다.

- 도박 연상 표현·사행성 UI·금전 보상 언어 사용 금지
- 건강·교육 언어만 사용
- 면책고지: "참고용 두뇌훈련 게임 · 의료적 진단이 아닙니다" 게임 화면 하단 상시 표시

### 요구사항 범위 확정

| 항목 | 포함 여부 | 비고 |
|---|---|---|
| 플레이어 손패 내기 애니메이션 | 포함 | 카드 선택 → 확대 → 바닥 이동 |
| 플레이어 더미 뒤집기 애니메이션 | 포함 (핵심 요구) | 확대 → 매치 강조 → 획득 이동 |
| AI 손패 내기 애니메이션 | 포함 | 사용자가 인식할 수 있는 속도 |
| AI 더미 뒤집기 애니메이션 | 포함 | AI 턴 전체 가시화 |
| 매치 없을 때 (바닥 내려놓기) | 포함 | 확대 → 페이드인 바닥 착지 |
| 속도 조절 옵션 | 포함 | 느림/보통/빠름 3단계 |
| 클릭 skip | 포함 (선택) | 애니메이션 도중 탭으로 skip |

---

## 2. 현재 FSM 구조 분석

### 현재 BH_GS.phase 상태값 (실측)

```
IDLE           → 게임 시작 전 (난이도 모달)
PLAYER_TURN    → 플레이어 손패 선택 대기
ANIMATING      → 전환 잠금 (onPlayerCardClick에서 사용 중)
AI_TURN        → AI 처리 중
GAME_OVER      → 게임 종료
```

### 현재 플레이어 턴 실행 흐름 (실측)

```
BH_onPlayerCardClick(card)
  └─ selectedCard 없음 → selectedCard 설정 → BH_renderBoard()
  └─ 매치 없음 → phase='ANIMATING' → setTimeout(BH_noMatchPlayerCard, 500ms)
  └─ BH_onFloorCardClick(floorCard) 호출됨
       └─ BH_captureCards(selected, floor, 'player')
       └─ setTimeout(BH_flipFromDeck_player, 700ms)

BH_flipFromDeck_player()
  └─ deck.shift() → deckFlipped
  └─ 매치 있음 → BH_captureCards(dc, matches[0], 'player') + BH_playCardMatch()
  └─ 매치 없음 → floor.push(dc) + BH_playCardPlace()
  └─ BH_renderBoard()
  └─ setTimeout(BH_finishPlayerTurn, 700ms)
```

### 현재 AI 턴 실행 흐름 (실측)

```
BH_doAITurn()
  └─ BH_aiSelectCard() → card
  └─ BH_playOpponentCard() (효과음만)
  └─ 매치 있음 → BH_captureCards(card, target, 'ai') + BH_renderBoard()
  └─ 매치 없음 → floor.push(card) + BH_renderBoard()
  └─ setTimeout(BH_flipFromDeck_ai, 600ms)

BH_flipFromDeck_ai(cb)
  └─ deck.shift() → dc
  └─ BH_playCardFlip()
  └─ 매치 있음 → captureCards + renderBoard
  └─ cb() → PLAYER_TURN 복귀
```

### 현재 문제점

현재 코드에서 `BH_renderBoard()`는 즉시 DOM 갱신이다. 사용자 눈에는 카드가 "순간이동"처럼 보인다. `setTimeout` 700ms 지연이 있지만, 중간 시각 단계(확대 → 겹침 → 이동)가 없다.

---

## 3. 변경 후 FSM 다이어그램

### 추가되는 FSM 단계

```
[현재]
PLAYER_TURN → (선택) → (매치) → captureCards → flipFromDeck → finishPlayerTurn → AI_TURN

[변경 후]
PLAYER_TURN
  └─ 손패 선택
       ↓
  ANIM_HAND_REVEAL    ← 신규: 플레이어 손패 카드 확대 표시 (800ms)
       ↓
  (매치 있음)           (매치 없음)
       ↓                    ↓
  ANIM_FLOOR_MATCH    ANIM_FLOOR_PLACE   ← 신규: 바닥 착지 (600ms)
  (바닥 카드 옆 겹침 600ms)
       ↓
  ANIM_CAPTURE        ← 신규: 획득 영역으로 이동 (700ms)
       ↓
  ANIM_DECK_FLIP      ← 신규: 더미 카드 확대 표시 (800ms)
       ↓
  (매치 있음)           (매치 없음)
       ↓                    ↓
  ANIM_DECK_MATCH     ANIM_DECK_PLACE    ← 신규: 바닥 착지 (600ms)
  (더미 카드 바닥 카드 옆 겹침 600ms)
       ↓
  ANIM_DECK_CAPTURE   ← 신규: 더미 획득 이동 (700ms)
       ↓
  finishPlayerTurn → AI_TURN
```

### AI 턴 변경 흐름

```
AI_TURN
  └─ aiSelectCard()
       ↓
  ANIM_AI_HAND_REVEAL     ← 신규: AI 손패 카드 확대 (플레이어 턴의 60% 시간)
       ↓
  (매치 있음/없음)
       ↓
  ANIM_AI_FLOOR_MATCH/PLACE ← 신규
       ↓
  ANIM_AI_CAPTURE           ← 신규 (매치 시)
       ↓
  ANIM_AI_DECK_FLIP         ← 신규
       ↓
  (매치 있음/없음)
       ↓
  ANIM_AI_DECK_MATCH/PLACE
       ↓
  ANIM_AI_DECK_CAPTURE (매치 시)
       ↓
  PLAYER_TURN 복귀
```

---

## 4. 단계별 타이밍 명세

### 기준 타이밍 (보통 속도 기준)

| 단계 | 이름 | 보통(ms) | 느림(ms) | 빠름(ms) | 설명 |
|---|---|---|---|---|---|
| 1 | 카드 확대 | 800 | 1500 | 600 | `BH_ANIM_REVEAL`: 카드 중앙 확대 팝업 |
| 2a | 매치 겹침 | 600 | 1000 | 400 | `BH_ANIM_MATCH`: 바닥 카드 옆 이동 |
| 2b | 바닥 착지 | 600 | 1000 | 400 | `BH_ANIM_PLACE`: 매치 없을 때 바닥 내려놓기 |
| 3 | 획득 이동 | 700 | 1200 | 500 | `BH_ANIM_CAPTURE`: 획득 영역으로 날아가기 |
| 4 | 더미 뒤집기 확대 | 800 | 1500 | 600 | `BH_ANIM_DECK_REVEAL`: 더미 카드 확대 팝업 |
| 5a | 더미 매치 겹침 | 600 | 1000 | 400 | `BH_ANIM_DECK_MATCH` |
| 5b | 더미 바닥 착지 | 600 | 1000 | 400 | `BH_ANIM_DECK_PLACE` |
| 6 | 더미 획득 이동 | 700 | 1200 | 500 | `BH_ANIM_DECK_CAPTURE` |

**플레이어 턴 전체 소요 시간 (보통, 매치 성공 기준)**:
800 + 600 + 700 + 800 + 600 + 700 = **4,200ms (약 4.2초)**

**AI 턴 전체 소요 시간 (보통, 매치 성공 기준)**:
AI 타이밍 = 플레이어 타이밍 × 0.6
480 + 360 + 420 + 480 + 360 + 420 = **2,520ms (약 2.5초)**

> AI 턴은 사용자가 결정권이 없는 구간. 길면 지루함 → 60% 단축 정책 적용.

### 속도 설정 저장

속도 선택은 `localStorage['BH_animSpeed']`에 저장. 게임 재시작 시에도 유지.

```javascript
// 속도 계수 정의
var BH_ANIM_SPEED = {
  slow:   { REVEAL: 1500, MATCH: 1000, PLACE: 1000, CAPTURE: 1200 },
  normal: { REVEAL: 800,  MATCH: 600,  PLACE: 600,  CAPTURE: 700  },
  fast:   { REVEAL: 600,  MATCH: 400,  PLACE: 400,  CAPTURE: 500  }
};
var BH_animSpeed = localStorage.getItem('BH_animSpeed') || 'normal';
```

---

## 5. 인터페이스 약속 (라운드테이블 §4)

### 5-1. game → design_ui

CSS keyframe 클래스 이름 및 트리거 조건:

| CSS 클래스명 | 트리거 조건 | 시각 효과 |
|---|---|---|
| `.BH_anim_reveal` | 카드 확대 표시 단계 시작 | scale(1→2.2) + 중앙 위치 + drop-shadow |
| `.BH_anim_match_move` | 매치 카드 옆으로 이동 | translate → 대상 카드 좌표 + 살짝 겹침(8px) |
| `.BH_anim_place` | 바닥 착지 (미스) | 바닥 빈자리로 translate + 투명도 0→1 |
| `.BH_anim_capture` | 획득 영역 이동 | translate → 획득 영역 + scale(2.2→0.8) |
| `.BH_anim_deck_flip` | 더미 카드 뒤집기 확대 | rotateY(0→180→0) + scale 확대 |
| `.BH_anim_ai` | AI 턴 클래스 수식어 | `.BH_anim_reveal.BH_anim_ai` → 상단에 "AI가 뒤집었어요" 레이블 |

**design_ui 구현 요청 사항**:
- 확대 카드는 `.BH_overlay_card` 컨테이너에 표시 (z-index: 200, 게임판 중앙)
- 오버레이 카드 최소 크기: 120px × 168px (카드 비율 5:7 유지)
- 모바일 기준: `max-width: min(240px, 80vw)`
- 레이블 텍스트: 18px 이상 (시니어 가독성)
- 카드 확대 시 배경 반투명 딤처리: `rgba(0,0,0,0.35)` 오버레이

**CSS keyframe 예시 (design_ui가 구현 기준으로 사용)**:

```css
@keyframes BH_kf_reveal {
  0%   { transform: scale(1);   opacity: 0.7; }
  30%  { transform: scale(2.2); opacity: 1; }
  80%  { transform: scale(2.2); opacity: 1; }
  100% { transform: scale(1);   opacity: 1; }
}

@keyframes BH_kf_capture {
  0%   { transform: scale(2.2) translateY(0);   opacity: 1; }
  100% { transform: scale(0.8) translateY(80px); opacity: 0.6; }
}

@keyframes BH_kf_deck_flip {
  0%   { transform: scale(1) rotateY(0deg);   }
  30%  { transform: scale(1) rotateY(90deg);  }
  60%  { transform: scale(2.2) rotateY(0deg); }
  80%  { transform: scale(2.2) rotateY(0deg); }
  100% { transform: scale(1) rotateY(0deg);   }
}
```

**애니메이션 완료 콜백 인터페이스 (design_ui → game)**:

```javascript
// design_ui가 구현하는 함수 시그니처
// game 에이전트는 이 함수를 호출하고, 콜백으로 다음 단계 진입
function BH_animateCardReveal(cardData, targetEl, onComplete) {
  // cardData: { id, month, type, emoji, name }
  // targetEl: 원본 카드 DOM 요소 (위치 기준)
  // onComplete: 애니메이션 완료 시 호출
}

function BH_animateCardMatch(revealEl, floorCardEl, onComplete) {
  // revealEl: 확대된 카드 오버레이 요소
  // floorCardEl: 매치 대상 바닥 카드 DOM 요소
  // onComplete: 겹침 완료 시 호출
}

function BH_animateCapture(cards, captureZoneEl, onComplete) {
  // cards: 획득할 카드 배열 [handCard, floorCard]
  // captureZoneEl: 획득 영역 DOM 요소
  // onComplete: 이동 완료 시 호출
}
```

### 5-2. game → sound

`BH_queueSound` 이벤트 키 (신규 포함):

| 이벤트 키 | 타이밍 | 설명 |
|---|---|---|
| `card_reveal` | 확대 시작 직후 | 카드 슬라이드업 효과음 (신규) |
| `card_flip` | 더미 뒤집기 시작 | 기존 BH_playCardFlip() 유지 |
| `card_match` | 매치 겹침 시작 | 기존 BH_playCardMatch() 유지 |
| `card_place` | 바닥 착지 완료 | 기존 BH_playCardPlace() 유지 |
| `card_capture` | 획득 이동 완료 | 획득 완료 효과음 (신규) |
| `ai_reveal` | AI 카드 확대 시작 | AI 전용 효과음 (신규, 다른 톤) |

sound 에이전트 구현 요청:
- `card_reveal`: 짧은 슬라이드업 톤 (150~200ms, C5 계열)
- `card_capture`: 가볍게 포착되는 느낌 (200ms, E5 계열)
- `ai_reveal`: `card_reveal`보다 낮은 톤 (A4 계열) → 내 패와 AI 패 청각 구분

---

## 6. 시니어 친화 옵션

### 6-1. 속도 토글 — 게임 시작 모달에 추가

난이도 선택 모달 하단에 속도 선택 행 추가:

```
[난이도 선택]
 [쉬움]  [보통]  [어려움]

[카드 속도]
 [느림]  [보통]  [빠름]
(현재 선택 강조 표시)
```

- 기본값: 보통
- 레이블 폰트: 16px 이상
- 버튼 높이: 44px 이상 (터치 타겟 기준)
- "느림" 선택 시 설명 1줄: "패를 천천히 확인하며 즐길 수 있어요"

### 6-2. AI 턴 단축화 정책

| AI 단계 | 보통 속도 | 이유 |
|---|---|---|
| AI 손패 확대 | 480ms (플레이어 800ms의 60%) | 결정권 없는 구간 — 짧게 처리 |
| AI 매치 겹침 | 360ms | 동일 이유 |
| AI 획득 이동 | 420ms | 동일 이유 |

> AI 턴이 너무 빠르면 무슨 일이 일어났는지 모름. 너무 느리면 지루함.
> 60% 시간이 "인식 가능하되 지루하지 않은" 최적값으로 설정.

### 6-3. 클릭 skip 기능

- 애니메이션 도중 게임판 탭/클릭 → 현재 애니메이션 단계 즉시 완료 + 다음 단계 진입
- `BH_GS.phase === 'ANIMATING'` 상태에서 클릭 이벤트 처리
- skip 시 효과음도 생략 (소리 중첩 방지)
- 단, REVEAL → MATCH 순서는 강제 유지 (중간 단계 건너뜀 불가)

```javascript
// skip 트리거 예시
function BH_skipAnim() {
  if (!BH_GS.animSkippable) return;
  BH_GS.animSkipRequested = true;
}
// game 에이전트가 각 setTimeout을 0으로 단축하는 방식으로 구현
```

### 6-4. 확대 카드 aria-live 안내

```html
<div id="BH_anim_live" aria-live="assertive" aria-atomic="true"
     style="position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden;">
</div>
```

확대 카드 표시 시 JavaScript로 텍스트 업데이트:
- 플레이어 더미 뒤집기: "더미에서 {월}월 {카드명} 패가 나왔습니다"
- AI 손패 내기: "AI가 {월}월 패를 냈습니다"
- 매치 성공: "{월}월 패 2장을 획득했습니다"

---

## 7. 모바일 대응

| 항목 | 명세 |
|---|---|
| 오버레이 카드 너비 | `min(240px, 80vw)` |
| 카드 비율 | 5:7 (width:height) 고정 |
| 오버레이 위치 | 게임판 중앙 (position: fixed, 320px 미만 기기도 대응) |
| 레이블 폰트 | `max(16px, 4vw)` |
| 터치 skip 영역 | 오버레이 카드 전체 영역 (min 44px × 44px 보장) |
| 가로모드 (landscape) | 오버레이 카드 위치 상단 1/3 영역 고정 |

---

## 8. QA 체크리스트

| # | 시나리오 | 확인 기준 | PASS |
|---|---|---|---|
| Q1 | 플레이어 손패 선택 → 매치 있음 | 확대(800ms) → 바닥카드 옆 겹침(600ms) → 획득 이동(700ms) 순서 정상 | |
| Q2 | 플레이어 손패 선택 → 매치 없음 | 확대(800ms) → 바닥 착지(600ms) 후 더미 뒤집기 진행 | |
| Q3 | 플레이어 더미 뒤집기 → 매치 있음 | 더미 카드 확대(800ms) → 바닥카드 옆 겹침(600ms) → 획득 이동(700ms) | |
| Q4 | 플레이어 더미 뒤집기 → 매치 없음 | 확대(800ms) → 바닥 착지(600ms) 후 AI_TURN 전환 | |
| Q5 | AI 턴 전체 | AI 패 확대(480ms) → 처리 → 더미 뒤집기 확대(480ms) 전체 가시화 | |
| Q6 | 느림 속도 설정 | 각 단계 타이밍 1.5~2× 정상 적용 | |
| Q7 | 빠름 속도 설정 | 각 단계 타이밍 0.6× 정상 적용 | |
| Q8 | 클릭 skip | 애니메이션 도중 탭 → 현재 단계 완료 후 다음 단계 즉시 진입 | |
| Q9 | 모바일 320px 폭 | 오버레이 카드 80vw 이내 표시, 레이블 잘리지 않음 | |
| Q10 | 더블클릭 차단 | ANIMATING phase 중 카드 클릭 무반응 확인 | |
| Q11 | aria-live 안내 | 스크린리더에서 "더미에서 8월 달광이 나왔습니다" 읽힘 확인 | |
| Q12 | 족보 달성 시 | 애니메이션 완료 후 족보 효과음 재생 (중첩 없음) | |
| Q13 | 게임 오버 직전 턴 | 마지막 카드 획득 애니메이션 완료 후 결과 화면 진입 | |
| Q14 | 게임 도중 포기 버튼 | ANIMATING phase 중 포기 → 강제 애니메이션 종료 + 결과 화면 | |

---

## 9. 검수 식별자

```
[검수 식별자:]
  - BH_animateCardReveal(cardData, targetEl, onComplete)
  - BH_animateCardMatch(revealEl, floorCardEl, onComplete)
  - BH_animateCapture(cards, captureZoneEl, onComplete)
  - BH_ANIM_SPEED (객체 — slow/normal/fast 계수)
  - BH_animSpeed (localStorage 연동 변수)
  - BH_skipAnim() (클릭 skip 트리거)
  - BH_anim_live (aria-live div ID)
  - .BH_anim_reveal / .BH_anim_match_move / .BH_anim_capture / .BH_anim_deck_flip (CSS 클래스)
  - .BH_overlay_card (확대 카드 컨테이너 CSS 클래스)
  - .BH_speed_btns (속도 선택 버튼 그룹 CSS 클래스)
```

SW 검수 (qa 에이전트 기준):
```javascript
typeof BH_animateCardReveal === 'function'  // PASS
typeof BH_animateCapture === 'function'     // PASS
typeof BH_ANIM_SPEED === 'object'           // PASS
```

---

## 10. BREAKS Footer

이 변경으로 기존 동작 중 변경/소멸되는 항목:

```
[BREAKS]
  - 즉시 카드 매치 처리 소멸: 현재 BH_captureCards() 호출 즉시 DOM 갱신 → 애니메이션 완료 콜백 후 갱신으로 변경
    (영향: game 에이전트가 captureCards 내부 setTimeout 구조 전면 변경 필요)

  - 한 판 예상 소요 시간 증가: 보통 속도 기준 턴당 약 4~8초 추가
    1판 평균 20턴 기준 → 전체 80~160초 추가 (1.5~2.5분 증가)
    (영향: 광고 체류 시간 증가 → 애드센스 노출 기회 증가, 긍정적)

  - ANIMATING phase 의미 변경: 현재 noMatchPlayerCard 처리 전용 →
    모든 카드 이동 단계 전반의 잠금 상태로 확장
    (영향: phase 체크 로직 수정 필요)

  - BH_renderBoard() 호출 시점 변경: 현재 즉시 → 각 애니메이션 완료 콜백 내부로 이동
    (영향: renderBoard 즉시 호출하던 위치 전면 검토 필요)

  - 속도 설정 UI 추가: 난이도 선택 모달 높이 증가 (약 60px)
    (영향: BH_diff_modal min-height 재조정 필요)
```

---

## 11. 태그 권장

```
plan/p7-card-anim-v1.0
```

태그 생성 커맨드 (lead 승인 후 실행):

```powershell
git tag -a plan/p7-card-anim-v1.0 -m "Post7 민화투 카드 인식 애니메이션 기획서 승인 — 2026-05-25"
git push origin plan/p7-card-anim-v1.0
```

---

## 부록 — 인지 훈련 가치

이 애니메이션 개선은 두뇌 트레이닝 효과를 직접 강화합니다:

| 인지 기능 | 개선 효과 |
|---|---|
| 시각 인식 | 확대 표시로 화투 패 식별 학습 기회 증가 |
| 주의력 | "어떤 패가 나왔나" 단계별 집중 포인트 제공 |
| 작업 기억 | 각 단계에서 패 정보를 기억할 충분한 시간 확보 |
| 패턴 인식 | 매치 과정 시각화 → 월(月) 패턴 학습 강화 |

면책고지: 이 게임은 참고용 두뇌훈련 게임입니다. 의료적 진단이 아닙니다.

---

*기획서 작성 완료: game_planner 에이전트 v1.9 / 2026-05-25*
*다음 단계: lead 검토·승인 → design_ui (CSS keyframe 구현) + sound (3종 효과음) → game (FSM 통합 구현)*
