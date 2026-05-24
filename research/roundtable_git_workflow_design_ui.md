# 라운드테이블 의견서 — design_ui 에이전트

**페르소나**: design_ui v1.7 (게임 UI 컴포넌트 전담)
**처리 시간**: progit_design_ui.md + design_ui.md 2회 Read 후 작성 완료 (동일 세션)
**작성일**: 2026-05-25

---

## §주제1: 화투게임(Post #7) git 관리 — UI 컴포넌트 관점

### 현재 구조의 핵심 문제

`widgets/post7_widget.html` 단일 파일에 design_ui가 납품한 HTML+CSS 컴포넌트와 game 에이전트의 JS 로직이 인라인으로 혼합되어 있다. 이 구조에서 design_ui 변경과 game 변경을 별도 커밋으로 분리하는 것은 `git add -p`를 써도 한계가 있다. 파일 자체가 단일 덩어리이기 때문이다.

### commit 단위에 대한 의견

design_ui 관점에서는 "분리 가능하지만 통합이 더 현실적"이라는 결론이다.

이유는 두 가지다. 첫째, CSS 컴포넌트와 JS 로직은 BH_card_selected 클래스 기준으로 밀접하게 결합되어 있다. CSS만 바꾸면 JS 동작이 달라지는 경우가 많다. 분리 커밋이 오히려 "반만 적용된 깨진 상태"를 git 이력에 남긴다. 둘째, wpautop 룰상 납품 시점에 이미 CSS가 단일행으로 minify된 상태라 `git add -p`로 CSS hunk만 분리하는 것이 비현실적이다.

현실적인 대안으로 다음을 제안한다:

- **개발 중**: design_ui가 `widgets/post7_ui_dev.html`(멀티라인 원본)을 독립 파일로 작업하고 `feat/p7-ui-{컴포넌트명}` 브랜치에 커밋. game은 이 파일을 참조해 로직 개발.
- **납품 시점**: design_ui 멀티라인 + game JS를 합산 minify → `widgets/post7_widget.html`에 통합 커밋. 커밋 메시지에 `[design_ui:컴포넌트목록] [game:변경내용]` 두 에이전트 책임 범위 병기.
- **버그 수정**: CLAUDE.md "타겟 PATCH" 룰과 동일하게, 위젯 파일 전체를 GET한 뒤 해당 CSS 규칙만 교체 후 커밋.

### pre-commit hook으로 검증할 수 있는 항목

다음 두 가지는 hook에서 자동화가 가능하다:

1. **BH_ prefix 검증**: `grep -E 'class="[^B]|id="[^B]'`로 BH_ 외 접두사 포함된 클래스·ID 검출 가능. WP 테마 기본 클래스(wp-block 등)는 제외 패턴 추가 필요.
2. **wpautop 단일행 검증**: `<style>` 태그 내부에 개행 문자(\n)가 있는지 Python으로 체크. 실패 시 minify 후 재실행 안내.

단, JS 이모지 Unicode escape 검증(`\u{xxxx}` 여부)은 이모지 패턴 목록이 방대해 hook보다는 game 에이전트 납품 전 수동 검증이 현실적이다.

---

## §주제2: 앞으로 게임 개발 워크플로우 — design_ui 관점

### 공통 컴포넌트 재사용 구조 제안

현재는 각 포스트 위젯 파일마다 BH_btn, BH_progress_wrap 등 공통 컴포넌트를 중복 인라인으로 포함하고 있다. 이 방식은 WP wp:html 블록 구조상 외부 파일 import가 불가하므로 단기적으로 변경 불가하다. 그러나 git 관리 차원에서는 다음 구조를 도입해 "중복의 단일 출처"를 만들 수 있다:

```
C:\Claude_code\widgets\
  _BH_common_ui.html      ← 공통 컴포넌트 원본 (minify 전 멀티라인)
  post6_widget.html       ← 공통 컴포넌트 인라인 포함 (minify 후)
  post7_widget.html       ← 공통 컴포넌트 인라인 포함 (minify 후)
```

`_BH_common_ui.html`이 SSOT(단일출처)가 되고, 각 포스트 위젯은 배포 시점에 공통 컴포넌트를 복사·통합한 결과물이 된다. 공통 컴포넌트가 변경되면 해당 커밋에서 "영향받는 포스트 위젯 목록"을 커밋 메시지에 명기하는 것으로 추적 가능성을 확보한다.

### design_ui → game 핸드오프 커밋 표준

```
[design_ui→game] post{N} UI 컴포넌트 납품

컴포넌트: {BH_card / BH_progress_wrap / BH_score_board / ...}
변경 이유: {신규 포스트 / 버그 수정 / 시니어 UX 개선}
영향 BH_ 클래스: {변경된 클래스명 열거}
wpautop 검증: style 단일행 PASS / 이모지 escape PASS
a11y 검증: 터치 타깃 44px+ PASS / WCAG AA 대비비 PASS
game 에이전트 수신 확인 필요: {게임 로직 연결 지점 명시}
```

### 시니어 a11y 검증을 git 워크플로우에 통합하는 방법

pre-commit hook에서 CSS 수치 검증은 어렵다(정규식으로는 계산된 값을 모른다). 대신 두 가지 방법을 조합한다:

- **정적 패턴 검증**: `min-height:\s*[0-9]+px`에서 숫자 추출 후 44 미만이면 경고. 이 정도는 hook에서 가능.
- **커밋 메시지 체크리스트 강제**: commit-msg hook에서 `a11y 검증:` 줄이 없으면 커밋 거부. 에이전트가 체크리스트를 의식적으로 포함하도록 강제하는 소프트 방법.

---

## §다른 에이전트에게 요청

**game 에이전트에게**: design_ui가 납품한 BH_ 클래스명을 JS 로직에서 직접 querySelector로 참조할 때, 클래스명 변경 시 사전 통보 없이 JS 내 하드코딩된 문자열만 수정하는 경우가 발생했다. 앞으로는 BH_ 클래스명 변경이 필요하면 design_ui에 먼저 알리고 CSS·JS 동시 업데이트를 단일 커밋으로 처리해 달라.

**design 에이전트에게**: SVG 화투 카드를 `BH_card_svg_wrap` 슬롯에 삽입할 때 SVG의 `width`·`height` 속성을 고정값으로 설정하면 clamp() 반응형이 무력화된다. SVG 파일 자체에는 `viewBox`만 설정하고 `width="100%"` `height="100%"`로 출력해 달라.

**sound 에이전트에게**: 효과음 트리거 함수는 design_ui가 정의한 이벤트 타이밍과 맞춰야 한다. 현재 BH_showFeedback(isCorrect) 호출 시점이 피드백 표시 즉시(0ms 지연 없음)이므로, 효과음도 이 함수 내부에서 즉시 재생하는 구조로 맞춰 달라. 0.8초 fade-out과 음원 길이를 일치시키면 더 좋다.

---

## §협업 약속 자가 점검

| 항목 | 상태 |
|---|---|
| 도박 연상 요소 0건 (BET, JACKPOT, 칩, 카지노 네온) | 확인 — 본 의견서에 해당 요소 없음 |
| 결과 화면 면책고지 필수 포함 | 유지 — 모든 컴포넌트 납품 시 BH_result_disclaimer 포함 |
| BH_ prefix 네이밍 일관성 | 유지 |
| CSS 단일행 wpautop 방어 | 유지 — 납품 시 필수 |
| 버튼 min-height 44px 이상 | 유지 |
| 커밋 메시지에 영향 BH_ 클래스 명시 | 신규 제안 — 본 의견서에서 표준화 제안 |
| 색상 토큰 SSOT | design_ui.md의 브랜드 컬러 시스템 테이블이 SSOT — design 에이전트와 충돌 시 design_ui.md 우선 (인터랙티브 요소 기준) |

### 색상 토큰 SSOT 입장 명확화

design 에이전트는 정적 PNG 카드 이미지 배경색을 관장하고, design_ui 에이전트는 인터랙티브 UI 컴포넌트 색상을 관장한다. 겹치는 영역(예: 카드 테두리 색상)이 발생하면 design_ui.md의 `--BH_border_card` 변수값을 기준으로 하되, design 에이전트 PNG 결과물이 이 색상과 시각적으로 일치하는지 QA 단계에서 확인하는 것이 현실적 분리 방법이다. git에서 두 에이전트가 같은 색상 헥스값을 별도 파일에 갖는 것은 중복이지만, 단일 파일로 합치면 에이전트 역할 경계가 무너진다는 점에서 현재 분리 구조를 유지하는 것이 옳다.
