# QA 검수 보고서 — Post #7 민화투 카드 인식 애니메이션
# 사전 검수 (WP PATCH 전 정적 코드 검수)

**검수 에이전트**: qa v8.57
**검수 일시**: 2026-05-25
**대상 파일**: `C:\Claude_code\widgets\post7_widget.html` (83,745 bytes, 96줄)
**기준 문서**: `C:\Claude_code\game_plans\post7_card_animation_plan.md` (v1.0)
**검수 단계**: 사전 검수 — WP PATCH 전 정적 grep 분석

---

## 협업 약속 자가 점검

| # | 약속 | 결과 | 비고 |
|---|------|------|------|
| 1 | lead 지시 범위 준수 | OK | 사전 검수(정적 분석)만 수행 — 직접 수정 없음 |
| 2 | 운영자 표기 룰 (neuralcare.co.kr) | OK | 코드 내 URL 패턴 확인 |
| 3 | YMYL 의료 단정 표현 0 | OK | 면책고지 텍스트 PASS |
| 4 | qa.md + 기획서 + 정본 위젯 사전 Read 완료 | OK | 3개 파일 모두 Read/grep 완료 |
| 5 | 자기 단계 인지 (사전 검수) | OK | WP PATCH 전 단계. 라이브 검증 제외 |
| 6 | 출력 형식 (박스·표·체크) | OK | 박스·표·PASS/FAIL 사용 |
| 7 | lead 단일 보고 | OK | 보고서 파일 생성 + lead 종합 판정 보고 |
| 8 | 도박 금지어 0건 확인 | OK | C1 항목 0건 PASS |

---

## A. 정적 코드 검수 결과

| # | 항목 | grep 결과 | 판정 |
|---|---|---|---|
| A1 | `function BH_animateCardReveal` | 94줄 1건 확인 | PASS |
| A2 | `function BH_animateCardMatch` | 94줄 1건 확인 | PASS |
| A3 | `function BH_animateCapture` | 94줄 1건 확인 | PASS |
| A4 | `function BH_animatePlace` | 94줄 1건 확인 | PASS |
| A5 | `function BH_animateDeckFlip` | 94줄 1건 확인 | PASS |
| A6 | `var BH_ANIM_SPEED=` 객체 정의 | 94줄 1건 확인 | PASS |
| A7 | `function BH_skipAnim` | 94줄 1건 확인 | PASS |
| A8 | `function BH_startWithDiff` (회귀) | 10·11·12·94줄 4건 확인 | PASS |
| A9 | style 태그 내부 개행 | 내부 1줄 — 단일 행 | PASS |
| A10 | script 태그 내부 개행 | 내부 1줄 — 단일 행 | PASS |
| A11 | 이모지 직접 사용 0건 (script 내) | script 내 `\u{1F...}` escape 18건 — 직접 이모지 0건 | PASS |
| A12 | `setAttribute('hidden')` 모달 사용 0건 | 1건 발견 — `BH_how_panel` 설명 토글 전용 (CLAUDE.md 예외 허용) | PASS (예외) |
| A13 | 48/48 카드 type↔svgUrl mismatch 0 | BH_DECK_DATA + svgUrl 존재 확인 / git 커밋 977f2ac 수정 완료 기록 / 단일 행 압축으로 전수 정적 검증 불가 — 동적 확인 필요 | CONDITIONAL |
| A14 | 면책고지 텍스트 존재 | "참고용 두뇌훈련 게임 · 의료적 진단이 아닙니다" 1건 확인 | PASS |

**A그룹 요약**: 13 PASS (A12 예외 인정) / 1 CONDITIONAL (A13 동적 확인 필요)

---

## B. 기획서 §8 QA 14종 시나리오 정적 분석

| # | 시나리오 | 분석 방법 | 판정 | 비고 |
|---|---|---|---|---|
| Q1 | 플레이어 손패 → 매치 있음 흐름 | `BH_animateCardReveal`·`BH_animateCardMatch`·`BH_animateCapture` 모두 정의 확인 | PASS (코드 경로 존재) | 타이밍 실측은 라이브 후 사용자 육안 확인 필요 |
| Q2 | 플레이어 손패 → 매치 없음 흐름 | `BH_animatePlace` + `BH_animateDeckFlip` 정의 확인 | PASS (코드 경로 존재) | 타이밍 실측은 라이브 후 |
| Q3 | 플레이어 더미 뒤집기 → 매치 있음 | `BH_animateDeckFlip`·`BH_animateCardMatch`·`BH_animateCapture` 정의 확인 | PASS (코드 경로 존재) | 타이밍 실측은 라이브 후 |
| Q4 | 플레이어 더미 뒤집기 → 매치 없음 | `BH_animateDeckFlip`·`BH_animatePlace` + AI_TURN 상태 전환 확인 | PASS (코드 경로 존재) | 타이밍 실측은 라이브 후 |
| Q5 | AI 턴 전체 — isAI 호출 | `isAI` 파라미터 패턴 1건 확인 | PASS (코드 경로 존재) | AI 60% 타이밍 실측은 라이브 후 |
| Q6 | 느림 속도 — BH_ANIM_SPEED.slow | `slow.*REVEAL` 패턴 1건 확인 — 객체 정의 존재 | PASS (정의 존재) | 실측은 라이브 후 |
| Q7 | 빠름 속도 — BH_ANIM_SPEED.fast | `fast.*REVEAL` 패턴 1건 확인 — 객체 정의 존재 | PASS (정의 존재) | 실측은 라이브 후 |
| Q8 | 클릭 skip — BH_skipAnim 트리거 | `BH_skipAnim` 3건 확인 / `ANIMATING` phase 체크 1건 확인 / `BH_GS.animSkip*` 변수명은 미확인 (단일 행 압축 한계) | CONDITIONAL | skip 트리거 이벤트 연결은 라이브 후 확인 |
| Q9 | 모바일 320px — 80vw 기준 | CSS에 `min(240px,80vw)` 1건 확인 | PASS | 시각 실측은 라이브 후 |
| Q10 | ANIMATING phase 더블클릭 차단 | `ANIMATING` 상태 체크 코드 1건 확인 | PASS (코드 경로 존재) | 실측은 라이브 후 |
| Q11 | aria-live — `BH_anim_live` | `aria-live` 9건 / `BH_anim_live` ID 존재 / `textContent` 갱신 코드 1건 확인 | PASS (정의 존재) | 스크린리더 실측은 라이브 후 |
| Q12 | 족보 달성 시 효과음 순서 | `BH_jokbo` 관련 코드 5건 존재 / 단일 행 압축으로 상세 순서 정적 미확인 | CONDITIONAL | 라이브 후 중첩 여부 확인 |
| Q13 | 게임 오버 직전 턴 | `GAME_OVER`·`BH_showResult`·`BH_result_modal` 각 3건 확인 | PASS (코드 경로 존재) | 실측은 라이브 후 |
| Q14 | 포기 버튼 ANIMATING 중 강제 종료 | "포기" 텍스트·`giveUp`·`quit` 패턴 0건 — 포기 버튼 미구현 가능성 | FAIL | 기획서 §8 Q14 명세 있으나 관련 코드 미검출 |

**B그룹 요약**: 10 PASS / 3 CONDITIONAL / 1 FAIL (Q14 포기 버튼)

---

## C. 도박 금지어 검수

| # | 검색 대상 | 검출 건수 | 판정 |
|---|---|---|---|
| C1 | 배팅·판돈·베팅·도박·사행·카지노·칩·캐시·잭팟 | 0건 | PASS |
| C2 | "내 패"·"AI 패"·"패가 나왔다" (화투 인용 허용) | — | 허용 |

---

## 특이사항 정리

### 1. A12 예외 처리 근거

`setAttribute('hidden', '')` 발견 위치:

```
)btn.setAttribute('aria-expanded','true');}else{p.setAttribute('hidden','');
```

이는 `BH_how_panel`(게임 방법 설명 토글) 패널 닫기 로직입니다. CLAUDE.md 규칙:
> "예외: `BH_how_panel` (설명 토글)은 테마 CSS 충돌 없어 `setAttribute('hidden')` 허용"
A12 PASS 처리.

### 2. B-Q14 FAIL — 포기 버튼 미구현 의심

기획서 §8 Q14: "게임 도중 포기 버튼 — ANIMATING phase 중 포기 → 강제 애니메이션 종료 + 결과 화면"

아래 패턴 전부 0건:
- "포기" (한글 텍스트)
- `giveUp`, `quit`, `abandon`, `BH_giveUp`

판정: 포기 버튼 기능이 위젯 코드에 없거나 다른 명칭 사용.
처리: game 에이전트에 확인 요청 또는 기획서 Q14가 이번 배포 범위 외인지 lead 확인 필요.

### 3. A13 CONDITIONAL — 카드 type↔svgUrl 전수 검증 불가

파일이 단일 행 압축(83,745 bytes, script 94줄)이므로 정적 grep으로 48장 전수 대조 불가.
이전 커밋 977f2ac("화투 카드 매핑 버그 수정 — 8월·12월")에서 수정 완료 기록 확인.
라이브 후 Chrome MCP javascript_tool로 `BH_DECK_DATA.length === 48` 동적 검증 필요.

### 4. 기획서 §3 FSM 신규 상태명 미발견

기획서에서 정의한 `ANIM_HAND_REVEAL`·`ANIM_FLOOR_MATCH`·`ANIM_FLOOR_PLACE`·`ANIM_CAPTURE`·`ANIM_DECK_FLIP` 상태명이 코드에서 0건입니다.

구현체가 다른 방식(예: `'ANIMATING'` 단일 상태 + 콜백 체인)으로 FSM을 처리했을 가능성이 있습니다. ANIMATING 상태는 1건 확인됩니다. 이는 기능 FAIL이 아니라 구현 방식 차이이며, 게임 동작 정확성은 라이브 후 확인이 필요합니다.

---

## 종합 판정

| 그룹 | 결과 |
|---|---|
| A. 정적 코드 검수 | 13 PASS / 1 CONDITIONAL |
| B. 기획서 시나리오 14종 | 10 PASS / 3 CONDITIONAL / 1 FAIL |
| C. 도박 금지어 | PASS |

**전체 판정: CONDITIONAL**

FAIL 항목(B-Q14 포기 버튼)은 기능 누락 의심 — lead 확인 후 게임 에이전트 보완 지시 또는 기획서 범위 재정의 필요.

---

## 라이브 후 필수 추가 검수 항목 (사전 검수 범위 외)

| # | 항목 | 확인 방법 |
|---|---|---|
| L1 | A13 카드 48장 전수 검증 | Chrome MCP: `BH_DECK_DATA.length === 48` |
| L2 | Q1~Q5 타이밍 실측 | Chrome MCP 게임 실행 후 단계별 ms 측정 |
| L3 | Q8 클릭 skip 동작 | Chrome MCP: ANIMATING 중 클릭 이벤트 발생 → 단계 즉시 완료 확인 |
| L4 | Q12 족보 효과음 순서 | Chrome MCP: 족보 달성 시 console.log 순서 확인 |
| L5 | Q14 포기 버튼 유무 | Chrome MCP: 포기 버튼 DOM 확인 또는 game 에이전트 재확인 |
| L6 | 모바일 320px 시각 검증 | Chrome DevTools Device 320px |
| L7 | 사운드 3종 신규 (card_reveal·card_capture·ai_reveal) | Chrome MCP AudioContext 실행 확인 |

---

*QA 보고서 작성: qa v8.57 / 2026-05-25*
*다음 단계: lead 검토 → (FAIL B-Q14 확인) → game 에이전트 보완 또는 기획서 범위 재정의 → WP PATCH*
