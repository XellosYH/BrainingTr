# git 워크플로우 라운드테이블 — design 에이전트 의견서

**작성일**: 2026-05-25
**작성자**: design 에이전트 v6.38
**대상**: 게임 관련 5개 에이전트 라운드테이블 (game / game_planner / design / design_ui / sound)
**처리 소요 시간**: 약 10분 (progit_design.md + design.md Read + 의견 작성)

---

## §주제1: 화투게임 git 관리 — 바이너리 자산 관점

### 핵심 주장: "SVG는 텍스트, PNG는 이력 주석으로 보완"

화투 SVG 48장은 텍스트 파일이다. git diff가 의미 있는 내용을 보여준다는 뜻이다. 반면 PNG export 결과물은 바이너리라 diff가 무력화된다. 이 두 성질이 design git 전략의 갈림길이다.

**SVG를 정본으로 관리하고, PNG는 export 산출물로 취급한다.**

구체적으로:

- git에 올리는 것: SVG 원본 전체 + PNG 최종 납품본 (body/og 2버전)
- .gitignore 처리: `*_draft.svg`, `*_working.svg`, `*.bak`, `html2canvas_tmp*` 등 중간 산출물 전량
- 커밋 메시지가 곧 PNG의 변경 이력이 된다. `"design: p7c01 body.png — 배경 흰색 전환 + 폰트 22px"` 형식으로 PNG 변경 내용을 커밋 메시지에 명시한다.

**git LFS 적용 시점 판단**:

현재(2026-05-25) 저장소 규모에서 LFS는 불필요하다. 포스트 50개 초과 또는 저장소 200MB 초과 시점에 dev 에이전트와 협의해 `git lfs track "design/*.png"` 도입을 검토한다. 화투 SVG 97장(48장 + 선택상태 48장 + 뒷면)은 SVG이므로 LFS 대상 아니다.

**body/og 2버전 분리와 git**:

동일 SVG 소스에서 배경색 전환(body: 흰 배경 / og: 청록 배경)으로 2버전을 export한다. SVG 레이어 혹은 CSS 변수 스위치 방식 중 어느 쪽이든, 소스 SVG 1개를 git에 관리하면 충분하다. PNG 2버전은 export 산출물로 둘 다 커밋한다. 파일명 suffix(`_body` / `_og`)가 용도를 명시하므로 추가 문서 없이 의도가 전달된다.

**시안 진화 추적 방법 — 태그 기반**:

바이너리 diff는 의미 없으므로 시안 버전 추적은 태그로 한다. 시안을 별도 브랜치나 폴더로 관리하는 방법도 있지만, design 에이전트가 단독으로 관리하는 단순 구조에서는 태그 방식이 오히려 깔끔하다.

```
hwatu-gwang-complete    (광 5장 완성 — game 테스트 가능 시점)
hwatu-48-complete       (전체 48장 완성)
design-p7-v1            (Post #7 카드 납품 1차)
design-p7-v2            (QA 지적 후 수정본)
```

폐기 시안은 별도 폴더(`design/_archive/`)에 보관하고 git에 올리지 않는다. git history에서 바이너리를 제거하는 `git filter-repo`는 복잡도가 높고 협업 위험이 크므로 권장하지 않는다.

**Edit 툴 SVG NUL 패딩 사전 차단**:

Edit 툴 수정 후 NUL 패딩이 발생한 SVG를 커밋하면 이후 렌더 실패가 발생한다. git commit 직전 `git diff --stat`으로 수정된 SVG 파일 크기 변동을 확인하고, 비정상적으로 크기가 커졌으면 NUL strip 검증을 선행한다. 이것이 design.md §산출물 검증 표의 "래스터화 전 NUL strip" 룰과 이어지는 git 단계 게이트다.

---

## §주제2: 앞으로 게임 개발 워크플로우 — design 관점

### commit 단위: 광 5장 묶음 → 순차 묶음 납품

카드 1장씩 커밋은 너무 잦고, 48장 완성 후 일괄 커밋은 중간 복구 포인트가 없다. 난이도 그룹별 묶음 커밋이 현실적이다:

1. 광 5장 완성 커밋 + `hwatu-gwang-complete` 태그 → game이 테스트 가능 상태
2. 열끗 9장 추가 커밋
3. 띠 10장 + 피 24장 완성 커밋 + `hwatu-48-complete` 태그

이렇게 하면 game이 전체 48장을 기다리지 않고 광 5장만으로 UI 레이아웃 테스트를 시작할 수 있다.

### git push가 납품 신호가 될 수 있는가

원칙적으로 태그 push가 납품 신호로 작동할 수 있다. 그러나 현재 협업 구조에서 에이전트 간 git 이벤트 자동 트리거가 없으므로, **태그 push + lead에 보고**를 병행한다. "태그 push만으로 충분"하다고 가정하면 lead가 인지를 놓칠 수 있다. 별도 보고는 생략 불가다.

### design이 다른 에이전트에게 요구하는 인터페이스 약속

**game 에이전트에게**: SVG 인라인 삽입 시 `src` 속성 직접 참조 방식은 경로 의존성을 만든다. SVG는 `wp:html` 블록 내 인라인으로 삽입하거나, PNG로 래스터화한 뒤 WP 미디어 ID 참조 방식을 쓸 것을 요청한다. SVG 파일 경로를 하드코딩해 `<img src="design/hwatu_svg/m01_gwang.svg">`로 참조하는 방식은 WP 환경에서 깨진다.

**dev 에이전트에게**: 카드 납품 시 body PNG 미디어 ID와 og PNG 미디어 ID를 항상 분리해 전달한다. dev가 두 ID를 혼용하지 않도록, 납품 보고서에 "body 미디어ID: XXX / og 미디어ID: YYY" 형식으로 명시한다.

**game_planner 에이전트에게**: 기획서에 카드 종류(광/조/피) 구분이 명시되어 있어야 design이 해당 SVG 제작 우선순위를 잡을 수 있다. "민화투 게임에서 실제로 사용하는 패 조합"이 기획서에 없으면 design이 전량 48장을 제작할지, 일부만 제작할지 판단이 불가능하다.

### 화투 SVG 재사용 — 공유 라이브러리 패턴 검토

화투 SVG가 향후 카드 매칭·기억력 게임에 재사용된다면 git submodule 방식보다 단순한 방법을 권장한다. 동일 저장소 내 `design/hwatu_svg/` 경로를 SSOT로 두고, 여러 게임 위젯이 이 경로를 참조하도록 약속하는 것이 더 관리가 쉽다. submodule은 clone 시 별도 초기화 단계가 필요하고, 1인 운영 구조에서 복잡도 대비 이득이 크지 않다.

---

## §다른 에이전트에게 요청

| 대상 | 요청 내용 |
|---|---|
| **game** | SVG를 `<img src>` 경로로 직접 참조하지 말 것. WP 환경에서 `wp:html` 인라인 또는 WP 미디어 ID 참조 방식만 사용 요청 |
| **game** | 광 5장 커밋 직후 `hwatu-gwang-complete` 태그로 중간 납품 테스트 시작 가능 여부 확인 요청 |
| **dev** | body/og 미디어 ID 혼용 방지를 위해 WP 업로드 후 두 ID를 분리 명시한 보고 양식 표준화 요청 |
| **game_planner** | 기획서에 "게임에서 사용하는 패 종류 목록(광/조/피 구분)"을 명시 요청 — design 제작 우선순위 결정에 필수 |

---

## §협업 약속 자가 점검

| 항목 | 상태 |
|---|---|
| design 본연 영역 의견만 작성했는가 | ✅ 바이너리 자산·SVG·PNG·라이선스·납품 인터페이스 관점만 |
| 다른 에이전트 의견 대변 0건인가 | ✅ game·sound·design_ui 의견 대변 없음 |
| 도박 연상 표현 0건인가 | ✅ "두뇌 트레이닝 게임 자산"으로만 언급 |
| 의료 단정 표현 0건인가 | ✅ 해당 없음 |
| 타 프로젝트 식별자 0건인가 | ✅ brain_health_1.0 전용 |
| 단순함 우선 — 불필요한 복잡도 추가 없는가 | ✅ submodule 대신 단일 경로 SSOT 권장 |

---

*저장 경로: `C:\Claude_code\research\roundtable_git_workflow_design.md`*
