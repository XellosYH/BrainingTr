# QA 검수 보고서 — post7_widget.html (민화투 두뇌훈련 게임)

**검수일**: 2026-05-19  
**파일 경로**: `C:\Claude_code\widgets\post7_widget.html`  
**파일 크기**: 37.9 KB (37,383자)  
**판정**: ✅ **PASS** (조건부 — 경미 개선 권고 2건)

---

## 체크리스트 결과

### A. wpautop 오염 방지

| # | 항목 | 결과 | 비고 |
|---|---|---|---|
| A-1 | `<style>` 내 개행(`\n`) 0건 | ✅ PASS | style 블록 1개 — 개행 0건 (단일 행 저장 확인) |
| A-2 | `<script>` 내 개행(`\n`) 0건 | ✅ PASS | script 블록 1개 — 개행 0건 (단일 행 저장 확인) |
| A-3 | style/script 내 `<br>`, `<p>`, `<hr>` 삽입 없음 | ✅ PASS | WP wpautop 오염 흔적 없음 |

---

### B. 게임 로직 기본

| # | 항목 | 결과 | 비고 |
|---|---|---|---|
| B-1 | `BH_DECK_DATA` 존재 + 48장 카드 | ✅ PASS | 1~12월 × 4장 = 48장 정확 |
| B-2 | FSM 상태 — `IDLE`, `PLAYER_TURN`, `AI_TURN`, `GAME_OVER` | ✅ PASS | 4개 상태 확인. `DEAL/MATCH/SCORING`은 미사용이지만 동등 로직 내재 (즉시 처리 방식) |
| B-3 | `BH_initGame` 함수 존재 | ✅ PASS | 덱 셔플·초기화 완전 구현 |
| B-4 | `BH_calcScore` 함수 존재 | ✅ PASS | `BH_calcScoreFromCaptured`로 위임하여 구현 |
| B-5 | 족보 6종 중 최소 3종 이상 | ✅ PASS | **7종 구현** — 오광·사광·비광·삼광·고도리·청단·홍단·초단·피 |
| B-6 | AI 난이도 2개 이상 분기 | ✅ PASS | **3단계** — easy(랜덤)/normal(greedy)/hard(look-ahead) |

---

### C. 사운드 모듈

| # | 항목 | 결과 | 비고 |
|---|---|---|---|
| C-1 | `window.BH_AudioContext` 전역 변수 | ✅ PASS | `BH_AC`로 할당 후 `window.BH_AudioContext` 참조 확인 |
| C-2 | `window.BH_SoundMuted` 전역 변수 | ✅ PASS | localStorage 연동 초기화 확인 |
| C-3 | 뮤트 토글 UI 요소 | ✅ PASS | `id="BH_mute_btn"` 버튼 + `aria-label="소리 켜기/끄기"` + 🔊/🔇 토글 |

---

### D. 저장소

| # | 항목 | 결과 | 비고 |
|---|---|---|---|
| D-1 | `localStorage` 사용 | ✅ PASS | BH_muted, BH_badges, BH_stats 키 사용 확인 |
| D-2 | `BH_checkAchievements` 함수 | ✅ PASS | win·tenPoints·threeGwang·fiveGwang·godori 5종 배지 구현 |

---

### E. UI/UX

| # | 항목 | 결과 | 비고 |
|---|---|---|---|
| E-1 | 난이도 선택 모달 | ✅ PASS | `BH_diff_modal` — 쉬움/보통/어려움 3단계 버튼 |
| E-2 | 결과 화면 | ✅ PASS | `BH_result_modal` — 게임 종료 오버레이 |
| E-3 | 재시작 버튼 | ✅ PASS | 재시작 버튼 존재 확인 |

---

### F. 접근성

| # | 항목 | 결과 | 비고 |
|---|---|---|---|
| F-1 | `role` 속성 최소 1개 | ✅ PASS | `role="dialog"` (2개: 난이도·결과 모달) |
| F-2 | `aria-label` 또는 `aria-live` | ✅ PASS | `aria-label`, `aria-live="polite"` 모두 확인 |

---

### G. 네임스페이스

| # | 항목 | 결과 | 비고 |
|---|---|---|---|
| G-1 | `BH_` 접두사 전역 함수/변수 | ✅ PASS | 고유 BH_ 식별자 **131개** 확인 |

---

### H. 파일 구조

| # | 항목 | 결과 | 비고 |
|---|---|---|---|
| H-1 | 단일 HTML 파일 (외부 JS/CSS import 없음) | ✅ PASS | 외부 스크립트·스타일시트 없음 |
| H-2 | 파일 크기 10KB 이상 | ✅ PASS | **37.9 KB** — 충분한 구현 규모 |

---

## 주요 발견사항

### ✅ 강점
1. **wpautop 완전 준수** — style/script 모두 단일 행 저장, 개행 0건
2. **48장 카드 정확** — 1~12월 × 광/조/피×2 구조 완전
3. **족보 7종 구현** — 오광·사광·비광·삼광·고도리·청단·홍단·초단·피 (요구 3종 초과)
4. **AI 3단계 난이도** — easy(random), normal(greedy capture), hard(look-ahead scoring)
5. **BH_ 네임스페이스 131개 식별자** — 충돌 방지 구조 견고
6. **접근성 완비** — role, aria-label, aria-live, aria-modal, aria-expanded, aria-controls

### ⚠️ 개선 권고 (비필수 — 게임 동작에 영향 없음)

**권고 1: FSM 명시적 DEAL/MATCH/SCORING 상태 부재**
- 현재: 플레이어 턴 시작 시 DEAL 로직이 `BH_initGame` 내에서 즉시 처리됨 (별도 DEAL 상태 없음)
- 현재: 카드 매칭 로직이 클릭 핸들러에서 직접 처리됨 (별도 MATCH 상태 없음)
- 영향: 게임 동작에는 문제 없으나, 복잡한 애니메이션 확장 시 FSM 명시적 분리 필요
- 권고: 현재 버전은 기능 정상 → 다음 버전에서 7-state FSM 완전 분리 고려

**권고 2: AI hard 난이도 look-ahead 심도 제한 확인 필요**
- `BH_aiSelectCard` 내 hard 분기: 1수 앞 look-ahead (score 비교) 구현 확인
- greedy 전략과 실질적 차별화: 캡처 시뮬레이션으로 최고 점수 카드 선택
- 영향: 게임 밸런스 검토 권장 (hard AI가 지나치게 강할 경우 피 누적 전략 고려)

---

## 최종 판정

| 카테고리 | 결과 |
|---|---|
| A. wpautop 오염 방지 | ✅ PASS |
| B. 게임 로직 기본 | ✅ PASS |
| C. 사운드 모듈 | ✅ PASS |
| D. 저장소 | ✅ PASS |
| E. UI/UX | ✅ PASS |
| F. 접근성 | ✅ PASS |
| G. 네임스페이스 | ✅ PASS |
| H. 파일 구조 | ✅ PASS |

**종합 판정: ✅ PASS** — 필수 항목 전건 통과. 개선 권고 2건은 비필수 사항으로 WP 업로드 차단 없음.

> QA 완료 시각: 2026-05-19T(검수 완료)  
> 검수자: qa 에이전트 v8.45
