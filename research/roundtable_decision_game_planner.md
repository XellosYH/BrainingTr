# 라운드테이블 2차 결정 표명서 — game_planner 에이전트

**페르소나**: game_planner v1.8
**처리 시간**: 5종 의견서 전량 Read 후 결정 표명 작성 — 약 2분
**참조 파일**: roundtable_git_workflow_game.md / roundtable_git_workflow_game_planner.md / roundtable_git_workflow_design.md / roundtable_git_workflow_design_ui.md / roundtable_git_workflow_sound.md

---

## Q1. 위젯 파일 구조 — 1순위: A

**선택**: A. 단일 정본 강제 (`widgets/post{N}_widget.html`만 git 관리)

**근거**:
CLAUDE.md "위젯 파일 단일 정본 룰"이 이미 확정된 상위 원칙이다. design_ui가 제안한 B안(개발용 분리본 + 납품용 통합 2단계)은 개발 편의성에서 장점이 있으나, 두 파일이 공존하는 순간 game 에이전트가 잘못된 베이스를 선택하는 사고(2026-05-25 v5b 커스텀 유실 사고)가 재발할 수 있다. game 의견서도 A안을 전제하고 있으며, 단일 정본 원칙과 마일스톤 커밋 전략을 결합하면 C안(영역별 분리)의 추적 이점도 커밋 메시지로 충분히 대체 가능하다.

**game_planner 영역 영향**: 기획서(`game_plans/post{N}_game_plan.md`)는 원래 단독 파일로 존재. 위젯 단일 정본 룰과 동일 원칙 적용 — 기획서 파일명에도 버전 suffix 금지. 버전 이력은 git 태그(`v1.0`, `v1.1`)로만 관리.

---

## Q2. LFS 도입 임계값 — 1순위: A

**선택**: A. 50포스트/200MB 초과 시

**근거**:
design 의견서(roundtable_git_workflow_design.md)가 제시한 기준을 그대로 지지한다. 현재 저장소는 초기 단계이며 LFS 도입은 복잡도를 높인다. 화투 SVG 97장은 텍스트 파일이므로 LFS 대상이 아니고, PNG 납품본만 바이너리다. 포스트 50개 초과 또는 200MB 초과 시점에 dev 에이전트와 협의해 `git lfs track "design/*.png"` 도입을 검토하는 유예 기준이 현실적이다.

**game_planner 영역 영향**: 기획서는 마크다운 텍스트이므로 LFS와 무관. 기획서 용량 이슈 발생 가능성 없음.

---

## Q3. pre-commit hook 작성 책임 — 1순위: B

**선택**: B. 단계적 도입

**근거**:
즉시 A안(dev 일괄 위임)을 선택하면 hook 작성 기준이 불명확한 채로 책임만 이전된다. game 의견서가 제시한 G1~G5 검증 게이트와 sound 의견서의 정적 분석 4개 항목, design_ui 의견서의 wpautop 단일행 검증은 각각 검증 로직이 다르다. 한 에이전트가 전부 처리하면 오류가 생겼을 때 책임 소재가 모호해진다. 단계적 도입: 1단계는 game G1(BH_ prefix)·G2(이모지 0건) 두 항목만 hook으로 자동화하고, 2단계에서 sound gain 검증, 3단계에서 wpautop 검증을 순차 추가한다.

**game_planner 영역 영향**: hook에 "기획서 [검수 식별자] 항목 존재 여부" 체크를 추가할 수 있다. 기획서에 `검수 식별자:` 줄이 없으면 `release:` prefix 커밋을 거부하는 hook이 기획-구현 연결 추적을 자동 강제한다. 1단계 hook 목록에 이 항목을 포함할 것을 제안한다.

---

## Q4. 인터페이스 약속 7건 .md 일괄 반영 — 1순위: A

**선택**: A. 7건 모두 즉시 일괄 반영

**근거**:
1차 의견서 5종에서 5개 에이전트 모두 인터페이스 약속을 명시했다. 이것이 .md 파일에 반영되지 않으면 다음 세션에서 컨텍스트 0 상태로 시작하는 에이전트가 약속을 모른 채 작업한다. 단계적 반영은 "어떤 약속이 반영됐고 어떤 게 대기 중인가"라는 추적 부담을 lead에게 떠넘긴다. 7건을 동시 반영하고 dev 에이전트가 해당 .md 파일을 일괄 수정 후 버전 bump + 스냅샷 + changelog 행 추가를 완료하는 것이 룰에 부합하는 처리다.

**game_planner 영역 영향**: game_planner.md에 반영될 인터페이스 약속 — (1) game이 기획서 승인 태그 기준 파일을 구현 기준으로 사용, (2) design/design_ui가 기획서 [UI 요구사항] 섹션 기준 승인 태그 확인, (3) sound가 기획서 [효과음 매핑] 섹션의 이벤트 key 명시 방식 준수.

---

## Q5. 태그 명명 규칙 통일 — 1순위: A

**선택**: A. 영역별 prefix 표준 통일

**근거**:
5개 에이전트 의견서에 이미 각자 다른 태그 명명이 등장했다. game_planner 의견서: `v1.0`, `v1.1`; design 의견서: `hwatu-gwang-complete`, `design-p7-v1`; sound 의견서: `sound-v1.5-post7`. 이 상태로 두면 어떤 태그가 어떤 에이전트의 어떤 포스트 마일스톤인지 `git tag -l`에서 즉시 파악 불가능하다. 표준 prefix:

| 에이전트 | 태그 형식 | 예시 |
|---|---|---|
| game_planner | `plan-p{N}-v{X.Y}` | `plan-p7-v1.0` |
| game | `game-p{N}-v{X.Y}` | `game-p7-v1.3` |
| design | `design-p{N}-v{X.Y}` | `design-p7-v1.0` |
| design_ui | `ui-p{N}-v{X.Y}` | `ui-p7-v1.0` |
| sound | `sound-p{N}-v{X.Y}` | `sound-p7-v1.5` |
| release | `release-p{N}-v{X.Y}` | `release-p7-v1.0` |

**game_planner 영역 영향**: 기획서 최초 승인 태그를 `plan-p{N}-v1.0` 형식으로 통일. 기존 의견서의 `v1.0` 단독 태그는 prefix 없이 release와 혼동 가능했으므로 수정 필요.

---

## 협업 약속 자가 점검

| # | 약속 | 상태 |
|---|---|---|
| 1 | 5종 의견서 전량 Read 후 결정 표명 작성 | ✅ |
| 2 | 다른 에이전트 의견 인용 시 출처 파일명 명시 | ✅ (design.md / sound.md 각 인용) |
| 3 | game_planner 자기 영역 관점만 표명 — 구현·디자인·사운드 대변 0건 | ✅ |
| 4 | 도박 연상 표현 0건 (배팅·판돈·잭팟 등) | ✅ |
| 5 | 기획서 파일명 버전 suffix 금지 원칙 재확인 | ✅ |
| 6 | 검수 식별자 hook 항목 제안 — 기획-구현 추적 자동 강제 | ✅ |
| 7 | 태그 prefix 제안이 기존 자기 의견서(단독 v1.0)와 일관성 있는지 확인 후 수정 명시 | ✅ |
