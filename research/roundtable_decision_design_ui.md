# 라운드테이블 2차 결정 의견서 — design_ui 에이전트

**페르소나**: design_ui v1.7 (두뇌 트레이닝 게임 UI 컴포넌트 전담)
**처리 시간**: 5종 의견서(game·game_planner·design·design_ui·sound) 교차 Read 후 결정 표명
**작성일**: 2026-05-25

---

## Q1. 위젯 파일 구조 — 1순위: B (개발용 분리본 + 납품용 통합 minify 2단계)

**근거**

1차 의견에서 제안한 방향이며, 5개 에이전트 의견을 교차 검토한 뒤에도 B가 옳다는 결론이 강화됐다.

game 에이전트는 "단일 정본 강제(A)"를 지지했으나, 그 전제는 game 관점의 논리다. design_ui 관점에서는 wpautop 단일행 강제 규칙이 핵심 문제다. minify된 단일행 파일에 CSS 컴포넌트 변경사항을 `git add -p`로 분리하는 것은 비현실적이다. BH_card_selected 클래스처럼 CSS와 JS가 밀접 결합된 구조에서 "반만 적용된 깨진 상태"를 커밋 이력에 남기는 것은 더 위험하다.

B 방식의 구체 구조:
- 개발 중: `widgets/_BH_common_ui.html` (공통 컴포넌트 멀티라인 원본), `widgets/post{N}_ui_dev.html` (포스트별 UI 원본)
- 납품 시점: minify 통합 후 `widgets/post{N}_widget.html` 단일 정본에 통합 커밋

**자기 영역 영향**: design_ui가 납품한 CSS 컴포넌트의 변경 이력이 `_BH_common_ui.html` diff로 명확히 추적된다. 현재처럼 minify된 위젯 파일 1행 diff에서 CSS 변경을 추적하는 것은 불가능하다.

---

## Q2. LFS 도입 임계값 — 1순위: A (50포스트/200MB 초과 시)

**근거**

design 에이전트가 제안한 기준과 동일하며, design_ui 관점에서도 동의한다. UI 컴포넌트는 순수 텍스트(HTML+CSS)이므로 design_ui 산출물 자체는 LFS 대상이 아니다. 바이너리 PNG를 생산하는 design 에이전트의 판단(50포스트/200MB)이 이 질문의 실질적 전문 영역이다.

design_ui 관점에서 추가할 것은 하나다. `_BH_common_ui.html` 공통 컴포넌트 파일은 텍스트이므로 LFS 도입 시에도 제외 대상으로 명확히 지정해야 한다. LFS는 바이너리 자산(PNG, WAV 등) 전용으로 제한하고 텍스트 파일은 기존 git 추적을 유지하는 것이 원칙이다.

**자기 영역 영향**: design_ui 산출물은 LFS 무관. 도입 이후에도 현재 워크플로우 변경 없음.

---

## Q3. pre-commit hook 작성 책임 — 1순위: B (단계적 도입)

**근거**

1차 의견에서 design_ui가 제안한 두 가지 hook 항목을 재확인한다.
- BH_ prefix 검증: `grep -E 'class="[^B]|id="[^B]'`로 구현 가능
- wpautop 단일행 검증: Python으로 `<style>` 태그 내 개행 문자 검출 가능

이 두 항목은 design_ui 핵심 도메인이며, dev 에이전트에 전량 위임(A)하면 검증 로직의 설계 의도가 희석될 위험이 있다. sound 에이전트도 gain 수치 grep 등 자기 영역 hook을 별도 제안했다. 각 에이전트가 자기 도메인 hook 명세를 작성하고, dev가 통합 구현하는 B 방식이 책임 소재를 명확히 한다.

단계 제안:
1. design_ui: BH_ prefix + style 단일행 hook 명세 작성
2. sound: gain 수치 + BH_SoundMuted 누락 + BH_getAC() 미경유 hook 명세 작성
3. game: G1(BH_ 네임스페이스)·G2(이모지 0건) hook 명세 작성
4. dev: 3개 에이전트 명세를 `.git/hooks/pre-commit` 단일 스크립트로 통합

도입 보류(C)는 v5b 베이스 선택 오류 같은 사고가 반복될 가능성이 있어 지지하지 않는다.

**자기 영역 영향**: design_ui가 hook 명세 작성 책임을 진다. dev에 "구현만 위임"하므로 도메인 의도 보존.

---

## Q4. 인터페이스 약속 7건 .md 일괄 반영 — 1순위: A (즉시 일괄 반영)

**근거**

5개 에이전트가 각자 의견서에서 명시한 인터페이스 약속들은 이미 충분히 논의되었다. 아래 7건은 design_ui 관점에서 모두 즉시 반영해야 한다.

1. game이 BH_ 클래스명 변경 시 design_ui에 사전 통보 (design_ui 1차 의견)
2. design SVG에 viewBox만 설정, width/height="100%" 출력 (design_ui 1차 의견)
3. sound가 BH_showFeedback() 타이밍에 맞춰 즉시 재생 (design_ui 1차 의견)
4. game이 BH_queueSound() 인터페이스로만 sound 호출 (sound 1차 의견)
5. design이 body/og 미디어ID를 분리 명시 보고 (design 1차 의견)
6. game_planner 기획서에 카드 종류(광/조/피) 구분 명시 (design 1차 의견)
7. game이 기획서 승인 태그 기준 파일 사용, 파일시스템 최신본 금지 (game_planner 1차 의견)

단계적 반영(B)은 "어떤 것을 나중에 하느냐"는 우선순위 결정 비용이 추가로 든다. 7건 모두 구현 부담이 크지 않고 이미 합의된 내용이므로 즉시 일괄 반영이 효율적이다.

**자기 영역 영향**: design_ui.md에 game·design·sound 인터페이스 약속 3건을 "수신 인터페이스" 섹션으로 추가. 즉시 실행 가능.

---

## Q5. 태그 명명 규칙 통일 — 1순위: A (영역별 prefix 표준 통일)

**근거**

5개 에이전트가 각자 다른 태그 명명을 제안했다.
- game: `game/post{N}-{기능명}` 브랜치
- game_planner: `v1.0`, `v1.1`, `v2.0` (기획서 버전)
- design: `hwatu-gwang-complete`, `design-p7-v1`
- sound: `sound-v1.5-post7`
- design_ui(1차): 별도 제안 없음

이 상태로 방치하면 `git tag -l`이 혼돈 상태가 된다. 영역별 prefix 통일(A)이 필요하다.

design_ui 제안 표준:

| 영역 | 태그 prefix | 예시 |
|---|---|---|
| game | `game/p{N}-` | `game/p7-fsm-complete` |
| game_planner | `plan/p{N}-` | `plan/p7-v1.0` |
| design | `design/p{N}-` | `design/p7-gwang-complete` |
| design_ui | `ui/p{N}-` | `ui/p7-card-component` |
| sound | `sound/p{N}-` | `sound/p7-v1.5` |
| 릴리스(WP 배포) | `release/p{N}-` | `release/p7-wp-put` |

`release/` prefix는 WP 실제 배포 완료 시점에 모든 에이전트가 공유하는 유일한 태그다. 영역별 자유(B)는 현재 문제를 그대로 두는 것이므로 지지하지 않는다.

**자기 영역 영향**: `ui/p{N}-` prefix 사용 즉시 적용. UI 컴포넌트 납품 완료 시점에 태그 생성이 design_ui의 명시적 책임이 된다.

---

## 협업 약속 자가 점검

| 항목 | 기준 | 확인 |
|---|---|---|
| 도박 연상 요소 0건 | BET·JACKPOT·칩·카지노 네온 없음 | 확인 |
| 두뇌 트레이닝 정체성 유지 | 의료·건강·교육 언어만 사용 | 확인 |
| design_ui 핵심 도메인(Q1·Q3) 근거 강화 | wpautop·BH_ prefix·a11y 관점 명시 | 확인 |
| 자기 영역 관점만 표명 | game JS 로직·sound 파라미터·design PNG 색상 대변 없음 | 확인 |
| 다른 에이전트 의견 대변 없음 | 교차 참조는 했으나 결론은 design_ui 관점 기준 | 확인 |
| 타 프로젝트 식별자 0건 | brain_health_1.0 전용 | 확인 |
