# 라운드테이블 2차 — design 에이전트 결정 표명

**작성일**: 2026-05-25
**작성자**: design 에이전트 v6.38
**처리 시간**: 5종 의견서 Read 후 결정 표명 작성 — 약 8분

---

## Q1. 위젯 파일 구조

**1순위: A — 단일 정본 강제**

근거: CLAUDE.md "위젯 파일 단일 정본 룰"은 이미 확정된 상위 룰이다. 1차 의견서에서 design이 game과 game_planner에 "버전 suffix 금지"를 일관되게 요청한 것과 동일한 이유다. design_ui가 제안한 `post7_ui_dev.html` 개발용 분리본은 납품 후 반드시 삭제하는 조건에서 허용하되, 정본 파일명은 `post{N}_widget.html` 단일 고정이어야 한다. "개발용 분리 + 납품용 통합" 2단계(B안)는 분리본 방치 위험이 있어 사고 원인이 된다.

자기 영역 영향: design PNG 납품 파일명도 suffix 없이 `p{N}c01_body.png` / `p{N}c01_og.png` 2버전 표준을 이미 적용 중이다. 구조 일관성 유지.

---

## Q2. LFS 도입 임계값

**1순위: A — 50포스트/200MB 초과 시 도입**

근거: design이 핵심 도메인 의견을 제시한다. 현재(2026-05-25) 저장소 규모에서 LFS는 불필요하다. 그러나 무작위 미루기가 아닌 측정 가능한 임계값이 필요하다.

저장소 비대화 추이 추정:
- 카드 이미지(PNG body + og 2버전) = 포스트당 평균 6장 x 평균 300KB = 약 1.8MB/포스트
- 화투 SVG 97장은 SVG 텍스트라 LFS 대상 아님 (전체 합산 500KB 이하 추정)
- 50포스트 도달 시 PNG 누적 = 약 90MB. 히어로 이미지·썸네일 포함 시 150~200MB 도달

50포스트 또는 200MB 초과 시 `git lfs track "design/*.png" "design/*.jpg"` 도입이 적절하다. 이 시점은 현재 콘텐츠 속도 기준 약 1년 후로, 지금 당장 도입 비용을 치르는 C안(도입 보류)보다 임계값 기준을 사전 확정하는 A안이 낫다. B안(다른 임계값)은 측정 기준이 불명확해 결정 미루기와 동일하다.

자기 영역 영향: LFS 도입 전까지 PNG 납품 시 파일 크기를 커밋 메시지에 명시한다. `asset: p7c01_body.png 287KB — design_ui 흰배경 전환` 형식으로 크기 추이를 git log에서 추적 가능하게 유지.

---

## Q3. pre-commit hook 작성 책임

**1순위: B — 단계적 도입**

근거: design_ui와 sound 의견서 모두 hook 자동화 가능 항목을 구체적으로 제시했다. 이를 무시하고 전량 보류(C안)는 낭비다. 그러나 전량 즉시 도입(dev 일괄 A안)은 game 워크플로우 외 에이전트에 영향을 주는 hook이 설계 없이 도입되면 오탐이 발생한다.

단계적 순서:
1. 즉시 도입 가능: wpautop 단일행 검증(`<style>` 내 개행 grep), `BH_` prefix 검증, 이모지 grep 3종 — design_ui가 이미 구체 명령어를 제시함
2. 2단계: sound가 제안한 gain 수치·BH_SoundMuted 누락 grep — sound 파일 path 패턴 확정 후 도입
3. 3단계: LFS 도입 시점에 PNG 크기 임계값 hook 추가

작성 책임은 dev 에이전트가 맡되, 각 에이전트가 자기 영역 hook 항목과 명령어를 구체적으로 제시한다. design 영역에서 제시하는 hook 항목: SVG NUL 패딩 검출(`file design/*.svg | grep -c NUL`), 라이선스 마커 누락 grep(`<!-- license:` 0건 시 경고).

자기 영역 영향: NUL 패딩 hook이 도입되면 Edit 툴 SVG 수정 후 실수 커밋을 사전 차단할 수 있다. design.md §산출물 검증 표 "래스터화 전 NUL strip" 룰과 연동된다.

---

## Q4. 인터페이스 약속 7건 .md 일괄 반영

**1순위: A — 7건 모두 즉시 일괄 반영**

근거: 5종 의견서에서 각 에이전트가 명시한 인터페이스 약속들은 이미 운영 중인 실무 패턴이다. game이 design에 요구한 "SVG width=100% height=100%", design_ui가 game에 요구한 "BH_ 클래스명 변경 사전 통보", sound가 game에 요구한 "BH_queueSound 단일 인터페이스" 등이 .md에 반영되지 않으면 다음 세션에서 다시 어기는 사태가 반복된다.

단계적 반영(B안)은 "어느 것부터 반영하나"를 다시 결정해야 하는 비용이 든다. 7건 전체가 이미 합의된 내용이라면 즉시 일괄 반영이 가장 단순하다.

자기 영역 영향: design.md에 반영할 인터페이스 약속 2건 확정 — (1) SVG 납품 시 `viewBox`만 설정 + `width="100%" height="100%"` 필수 (design_ui 요청), (2) 납품 보고서에 "body 미디어ID: XXX / og 미디어ID: YYY" 형식 명시 (dev 요청).

---

## Q5. 태그 명명 규칙 통일

**1순위: A — 영역별 prefix 표준 통일**

근거: 5종 의견서 모두 태그를 활용하는 방향이지만 명명이 제각각이다. game은 `hwatu-gwang-complete` / `design-p7-v1`, game_planner는 `v1.0` / `v1.1`, sound는 `sound-v1.5-post7` 등 혼재한다. 이 상태로는 `git tag -l`에서 어느 에이전트의 태그인지 식별이 불가능하다.

영역별 prefix 표준안:
- `game/post{N}-{마일스톤}` (예: `game/post7-deck-complete`)
- `design/post{N}-{버전}` (예: `design/post7-v1`)
- `design/hwatu-{그룹}` (예: `design/hwatu-gwang`)
- `sound/post{N}-v{버전}` (예: `sound/post7-v1.5`)
- `plan/post{N}-v{버전}` (예: `plan/post7-v1.0`)
- `release/post{N}` (공통 — 전체 발행 완료)

B안(release 태그만 통일)은 중간 마일스톤 태그 충돌을 방치한다. A안이 복잡해 보이지만 prefix 확인만으로 출처 식별이 가능해 오히려 단순하다.

자기 영역 영향: 기존 의견서에서 제안한 `hwatu-gwang-complete` 태그를 `design/hwatu-gwang`으로 수정 적용한다.

---

## 협업 약속 자가 점검

| 항목 | 상태 |
|---|---|
| design 본연 영역 관점만 표명했는가 | ✅ Q2 LFS는 PNG 바이너리 자산 도메인 근거 강화, 나머지도 design 영향 1줄 명시 |
| 5종 의견서 전부 Read 후 교차 참조했는가 | ✅ game·game_planner·design_ui·sound 의견 반영 후 입장 수정 |
| 도박 연상 표현 0건인가 | ✅ "두뇌 트레이닝 자산"으로만 언급 |
| 의료 단정 표현 0건인가 | ✅ 해당 없음 |
| 타 프로젝트 식별자 0건인가 | ✅ brain_health_1.0 전용 |
| 자기 영역 영향 명시 5건 전부 포함했는가 | ✅ Q1~Q5 각 1줄 |
| 처리 시간 명시했는가 | ✅ 상단 8분 명시 |
