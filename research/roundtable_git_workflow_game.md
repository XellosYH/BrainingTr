# 라운드테이블 의견서 — game 에이전트 관점
# 주제: 화투게임 git 관리 + 5개 에이전트 협업 워크플로우

**작성 에이전트**: game (두뇌 트레이닝 게임 위젯 개발)
**처리 시간**: progit_game.md + game.md(상단) Read 후 의견서 작성 — 약 3분

---

## §주제1 — 화투게임 git 관리 (Post #7 기준)

### 커밋 타이밍 — 마일스톤 기준 제안

위젯 단일 파일(`widgets/post7_widget.html`) 특성상 코드량이 1,000~1,500줄이다. 중간 저장 없이 전체 완성 후 커밋하면 롤백 단위가 너무 크다. game 영역에서 아래 마일스톤 단위로 커밋한다:

| 순서 | 마일스톤 | 커밋 메시지 예시 |
|---|---|---|
| 1 | BH_DECK_DATA + BH_dealCards 완성 | `feat: post7 화투 덱 48장 데이터 + 딜링 함수 완성` |
| 2 | FSM 7상태 + BH_renderAll 완성 | `feat: post7 FSM 게임 상태 머신 + 전체 렌더링 완성` |
| 3 | 족보 판정 + 점수 계산 완성 | `feat: post7 족보 판정 BH_checkJokboComplete + 점수 계산 완성` |
| 4 | AI 3난이도 완성 | `feat: post7 AI Easy/Normal/Hard 분기 완성` |
| 5 | 난이도 모달 + 결과 화면 완성 | `feat: post7 BH_showDifficultyModal + 결과 화면 완성` |
| 6 | minify 적용 완료 | `build: post7 위젯 minify 완료 WP PUT 준비` |
| 7 | WP PUT 성공 확인 | `deploy: post7 위젯 WP 업로드 완료 (페이지 ID 303)` |

마일스톤 1~5 사이에 버그 수정 발생 시 즉시 별도 커밋. 로직 변경과 minify를 절대 같은 커밋에 넣지 않는다.

### 브랜치 전략

brain_health는 1인 운영이므로 main 직접 커밋을 기본으로 한다. 예외:

- **topic 브랜치 생성 조건**: 민화투 v2(대규모 기능 추가) 또는 신규 게임 위젯 추가 시
- **topic 브랜치 명**: `game/post{N}-{기능명}` 형식 (예: `game/post7-nback-mode`)
- 단순 버그 수정·CSS 조정은 main에 직접 커밋

### 사고 방지 — v5b 베이스 선택 오류 재발 방지

2026-05-25 game 에이전트가 구버전 v5b를 베이스로 선택해 커스텀 유실 사고 발생. 재발 방지 절차:

1. **작업 전 필수 확인**: `git log --oneline widgets/post7_widget.html` 실행 — 최신 커밋 SHA 확인
2. **파일명 suffix 절대 금지**: `widgets/post7_widget.html` 단일 정본만 존재. 다른 파일명이 보이면 즉시 삭제 또는 무시
3. **작업 시작 직전 커밋**: 기존 코드를 보존 커밋한 뒤 수정 시작 — 실패해도 한 커밋 롤백으로 복원 가능

### 롤백 정책

`git reset --hard` 사용 금지. 파일 단위 복원을 원칙으로 한다:

```powershell
git log --oneline widgets/post7_widget.html   # 복원 대상 SHA 확인
git checkout {SHA} -- widgets/post7_widget.html
git commit -m "revert: post7 위젯 {이유} 시점으로 복원"
```

게임 동작이 전혀 안 깨진 마지막 커밋(보통 이전 마일스톤 커밋)이 롤백 기준점이다. WP PUT 전 커밋이 항상 안전 기준점 역할을 한다.

---

## §주제2 — 5개 에이전트 협업 워크플로우

### 각 에이전트의 commit 책임 영역

| 에이전트 | 커밋 대상 | prefix |
|---|---|---|
| **game** | `widgets/post{N}_widget.html` | `feat/fix/style/build/deploy` |
| **game_planner** | `game_plans/post{N}_game_plan.md` | `docs` |
| **design** | `design/p{N}c*.png` (body + og 2버전) | `asset` |
| **design_ui** | `widgets/post{N}_ui.html` 또는 game에 직접 전달 시 커밋 불필요 | `asset` |
| **sound** | `widgets/post{N}_sound.js` (별도 파일) 또는 game 위젯에 인라인 시 game 커밋에 포함 | `asset` |

game 위젯은 단일 HTML 파일이므로, design_ui와 sound 산출물을 위젯에 인라인 통합하는 시점의 커밋이 사실상 3개 에이전트의 결과물을 동시에 기록한다. 이 커밋 메시지에 어떤 에이전트 산출물이 통합되었는지 명시한다:

```
feat: post7 sound 모듈 + design_ui 컴포넌트 위젯 통합

- BH Sound Module v1.2 (sound 에이전트) 인라인 적용
- 난이도 모달 UI (design_ui 에이전트) 적용
- 위젯 파일: widgets/post7_widget.html
```

### 커밋 순서 및 의존성

```
[game_planner] docs: post7 게임 기획서 완성
        ↓ (기획서 확정 후 game 착수 가능)
[design]   asset: post7 화투 카드 48장 PNG body/og 완성
[sound]    asset: post7 효과음 JS 모듈 완성
[design_ui] asset: post7 UI 컴포넌트 블록 완성
        ↓ (3개 에이전트 병렬, 모두 완료 후)
[game]     feat: post7 위젯 마일스톤 1~5 순차 커밋
[game]     build: post7 minify 완료
[game]     deploy: post7 WP 업로드 완료
```

game_planner 기획서가 확정되어야 game이 착수할 수 있다. design·sound·design_ui는 기획서 기반으로 game과 병렬 진행 가능하다. 단, game이 이들의 산출물을 통합하는 시점은 game 코드 기본 골격(FSM + 덱 데이터) 완성 이후다.

### 검증 게이트 (game 기준)

game이 WP PUT 전 통과해야 하는 검증:

| 게이트 | 검증 항목 | 방법 |
|---|---|---|
| G1 | BH_ 네임스페이스 전수 확인 | `grep -c 'function [^B]' widget.html` = 0 |
| G2 | JS 이모지 0건 | Python `emoji_count == 0` |
| G3 | style/script 단일 행 | `wc -l <style>` 내용 = 1행 |
| G4 | 외부 통신 0건 | `grep -c 'fetch\|XMLHttpRequest\|cdn' widget.html` = 0 |
| G5 | 면책 문구 존재 | `grep '참고용 두뇌훈련'` 검출 |

G1~G5 전부 통과 후에만 `build:` 커밋 생성. 미통과 시 게이트 항목 수정 후 재검증.

---

## §다른 에이전트에게 요청하는 인터페이스 약속

### game이 요구하는 것 (수신 인터페이스)

**1. game_planner에게**
기획서(`game_plans/post{N}_game_plan.md`) 납품 시 아래 항목을 반드시 포함해야 한다:
- 인지 기능 도메인 명시 (예: "작업기억·패턴인식·계산력")
- WP 검수 식별자 (예: `BH_startWithDiff`) — SW 게이트 검증에 필요
- 난이도 3단계 정의 (Easy/Normal/Hard 동작 차이)

**2. design에게**
카드 PNG 납품 시:
- 파일명: `p{N}c{NN}_body.png` / `p{N}c{NN}_og.png` 2버전 필수
- body 버전: 흰 배경, 카드명 18px 이상, WCAG AA 대비
- id 데이터: WP 미디어 업로드 후 미디어 ID 목록을 game에 전달 (위젯 내 이미지 참조에 필요)

**3. sound에게**
BH Sound Module JS 블록 납품 시:
- 이모지 0건 (wp_staticize_emoji 대응)
- AudioContext 싱글톤 패턴 필수 (모바일 정책 대응)
- 뮤트 토글 전역 변수 `window.BH_SoundMuted` 연동 확인

### game이 약속할 수 있는 것 (발신 인터페이스)

**1. QA에게**: 위젯 납품 시 G1~G5 검증 게이트 통과 결과표를 함께 전달한다. "통과" 주장 없이 수치 근거 제시.

**2. dev에게**: WP PUT 전 `build:` 커밋 SHA를 전달한다. dev는 이 SHA 기준 파일을 PUT한다. 로컬 최신 파일이 아닌 커밋 기준 파일 사용 — stale data 위험 차단.

**3. game_planner에게**: 기획서 항목 구현 불가 판정 시(기술적 한계·코드 규모 초과) 즉시 협의 요청한다. 임의 변경 없이 기획서와 위젯 간 불일치를 game_planner에 보고한다.

---

## §협업 약속 자가 점검

| # | 약속 | 점검 |
|---|---|---|
| 1 | game 영역(위젯 HTML/JS/CSS)만 커밋 — 기획서·PNG·효과음은 해당 에이전트 책임 | 확인 |
| 2 | 마일스톤 단위 커밋 — 전체 완성 후 일괄 커밋 금지 | 확인 |
| 3 | minify와 로직 변경은 별도 커밋 | 확인 |
| 4 | 작업 전 `git log --oneline`으로 최신 SHA 확인 (v5b 사고 재발 방지) | 확인 |
| 5 | G1~G5 게이트 통과 후에만 `build:` 커밋 | 확인 |
| 6 | 도박·사행성 표현 0건 — 화투 = 인지 강화 훈련 도구 | 확인 |
| 7 | 다른 에이전트 의견 대변 금지 — game 관점만 명확히 | 확인 |
