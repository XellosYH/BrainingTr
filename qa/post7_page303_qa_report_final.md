# QA 보고서 — 민화투 두뇌훈련 게임 허브 페이지

**페이지**: https://neuralcare.co.kr/brain-games/minwhatoo/  
**Page ID**: 303  
**검수 일시**: 2026-05-22  
**검수 에이전트**: qa v8.56  
**파이프라인**: 게임 전용 허브 페이지 검수 (§ 게임 전용 검수 파이프라인)

---

## 최종 판정: ✅ PASS

---

## 검수 항목별 결과

| 항목 | 기준 | 결과 | 비고 |
|---|---|---|---|
| S1 (본문 500자) | 게임 허브 페이지 — 예외 적용 | ✅ 예외 | `/brain-games/` 경로 → S1 면제 |
| S3 (Mojibake 0건) | `ë`, `ì`, `í`, `ê¸` 등 0건 | ✅ PASS | 전체 HTML 포함 0건 확인 |
| SW (BH_ 함수 6종) | 전부 "function" | ✅ PASS | 6종 전부 확인 |
| 게임 실행 확인 | 난이도 선택 → 게임 보드 전환 | ✅ PASS | 쉬움·보통 양쪽 확인 |
| 재시작 버튼 | BH_restartGame() → 난이도 모달 복귀 | ✅ PASS | 정상 동작 확인 |
| 도박 금지어 | 배팅·판돈·도박·사행·카지노 0건 | ✅ PASS | 0건 확인 |
| 면책 문구 | "참고용 두뇌훈련 게임 · 의료적 진단이 아닙니다" | ✅ PASS | result_modal 내 존재 확인 |
| 모바일 레이아웃 | viewport meta 설정 | ✅ PASS | `width=device-width, initial-scale=1` |

---

## 세부 검증 결과

### S3 — Mojibake 0건 ✅

```
확인 패턴: ë, ì, í, ê¸, â, ã, å, ç
결과: 전부 0건 (document.documentElement.innerHTML 전체 검사)
```

### SW — BH_ 함수 6종 ✅

```
BH_startWithDiff = function ✅
BH_restartGame = function ✅
BH_confirmNewGame = function ✅
BH_startAutoTimer = function ✅
BH_showHint = function ✅
BH_toggleHow = function ✅
```

### 게임 실행 확인 ✅

**초기 상태**:
- BH_diff_modal: display=flex (난이도 선택 모달 표시)
- BH_game_board: display=none

**쉬움 난이도 선택 후**:
- BH_diff_modal: style=none, computed=none ✅
- BH_game_board: computed=block ✅

**보통 난이도 선택 후**:
- BH_diff_modal: computed=none ✅
- BH_game_board: computed=block ✅
- floor_cards=8, hand_cards=8, 덱=24, 턴=내 차례 ✅

**BH_GS 상태**: 글로벌 BH_GS 객체 미존재 — 게임 상태는 DOM 기반으로 관리됨
- BH_deck_count: "덱 24" ✅
- BH_floor_zone: 카드 8장 ✅
- BH_hand_zone: 카드 8장 ✅
- BH_turn_info: "내 차례" ✅

### 재시작 버튼 ✅

- BH_restartGame() 클릭 → BH_diff_modal: flex (난이도 선택 모달 복귀) ✅
- BH_confirmNewGame() 버튼도 정상 존재 ✅

### 도박 금지어 0건 ✅

```
검사 항목: 배팅, 판돈, 도박, 사행, 카지노
결과: 0건
```

### 면책 문구 ✅

BH_result_modal 내 텍스트:
```
"참고용 두뇌훈련 게임 · 의료적 진단이 아닙니다"
```
- disclaimer1(참고용 두뇌훈련 게임) = true ✅
- disclaimer2(의료적 진단이 아닙니다) = true ✅

### 모바일 레이아웃 ✅

```
viewport meta: width=device-width, initial-scale=1
```

---

## 특이 사항

1. **BH_GS 전역 객체 미존재**: qa.md 검증 스크립트에서 `BH_GS.phase` 등을 확인하도록 되어 있으나, 해당 구현은 전역 BH_GS 객체 대신 DOM 요소(BH_deck_count, BH_floor_zone, BH_hand_zone, BH_turn_info)로 상태를 관리. 게임은 정상 작동하므로 구현 방식의 차이로 판단. 기능적 PASS 처리.

2. **sStyle.display 방식**: diff_modal은 `style.display='none'` 방식으로 제어됨 (CLAUDE.md WP CSS 특이성 룰 준수 ✅)

---

## 검수 완료 타임스탬프

`2026-05-22T00:00:00` (검수 일자 기준)

---

**최종 판정: ✅ PASS — 발행 유지 적합**
