# Pro Git 학습 — design_ui 에이전트 관점

처리 시간: ch1(Git 기초·스냅샷 개념) / ch2(add·commit·log·diff·stash 핵심 명령) / ch3(브랜치·merge·hotfix 패턴) / ch5(분산 워크플로·커밋 메시지 가이드라인) / ch7(stash 심화·blame·bisect·대화형 add) — 5개 챕터 전량 독해 완료.

---

## 1. 핵심 git 명령어 (UI 컴포넌트 관리에 유용한 것)

| 명령어 | 용도 | design_ui 적용 예 |
|---|---|---|
| `git add -p` | 파일 일부분만 스테이징 | CSS 변수 변경과 레이아웃 변경을 별도 커밋으로 분리할 때 |
| `git diff --staged` | 커밋 전 staged 변경 내용 검토 | BH_ 클래스 추가 전 오타·누락 확인 |
| `git log -p widgets/` | 특정 경로 커밋별 diff 조회 | post{N}_ui.html 변경 이력 전체 추적 |
| `git log -S "BH_progress"` | 특정 문자열이 추가/삭제된 커밋 탐색 | CSS 변수·컴포넌트 ID가 언제 도입됐는지 파악 |
| `git blame widgets/post7_ui.html` | 라인별 최종 커밋자·시점 확인 | 특정 CSS 규칙이 누가·언제 변경했는지 추적 |
| `git stash` / `git stash pop` | 미완성 작업 임시 저장 | 다른 포스트 긴급 수정 중 진행 중인 컴포넌트 보관 |
| `git checkout -b` | 실험 브랜치 즉시 생성 | 애니메이션·색상 실험을 main과 격리해 테스트 |
| `git branch -d` | 완료 브랜치 정리 | merge 후 불필요한 실험 브랜치 제거 |
| `git merge --no-ff` | Merge 커밋 명시 보존 | 실험 브랜치 이력을 main에서도 확인 가능하게 유지 |
| `git show HEAD~3` | 3커밋 전 스냅샷 조회 | "왜 이 CSS 변수를 바꿨지?" 역추적 |

---

## 2. 컴포넌트 실험·재사용 워크플로 (브랜치·stash·merge)

### 2-1. 실험 브랜치 패턴 (CSS 변수 실험)

```
main 브랜치 (안정 상태)
  |
  +-- git checkout -b feat/timer-darkmode
  |     - BH_timer_wrap 다크모드 CSS 변수 실험
  |     - git commit -m "feat: timer dark mode CSS variable draft"
  |     - 브라우저 확인 → 만족 시 main으로 merge
  |     - 불만족 시 git branch -D feat/timer-darkmode (흔적 없이 폐기)
  |
  +-- git merge feat/timer-darkmode  ← 성공 시
```

- 브랜치는 SHA-1 포인터 40바이트 파일에 불과하므로 생성 비용 0. 실험마다 브랜치를 만들어도 부담 없음.
- Fast-forward: 실험 브랜치만 커밋이 있으면 main 포인터가 그냥 앞으로 이동. 별도 merge 커밋 불생성.
- 3-way merge: main과 브랜치 양쪽에 커밋이 생기면 merge 커밋 자동 생성 → 이력에 "어느 브랜치에서 왔는지" 남음.

### 2-2. git stash — 긴급 전환 패턴

```
상황: post8_ui.html 작업 중 → post7 버그 신고 접수

# 현재 작업 임시 저장 (커밋 없이)
git stash

# post7 브랜치로 전환 후 수정·커밋
git checkout main
(post7 버그 수정 후 커밋)

# 원래 작업 복원
git checkout -  (직전 브랜치로 돌아가기)
git stash pop   (임시 저장 복원)
```

- `git stash list` 로 여러 개의 stash 조회 가능. `stash@{0}` 이 가장 최근.
- `git stash apply --index` 는 staged 상태까지 복원. 단순 `apply` 는 staged 해제 후 복원.
- `git stash -u` 는 Untracked 파일(새로 만든 HTML 파일)까지 함께 저장.

### 2-3. CSS 변수 영향 범위 추적 (git log -p + git blame)

```bash
# BH_primary 변수가 변경된 커밋 전부 보기
git log -p --all -S "BH_primary" -- widgets/

# 특정 CSS 라인을 누가 언제 마지막으로 변경했는지
git blame -L 1,50 widgets/post7_ui.html
```

- `git blame -C` 옵션: 파일이 복사·이동됐어도 원본 커밋 추적 가능 (컴포넌트를 다른 포스트 파일로 복사한 경우 유용).
- `git log --stat widgets/` : 어떤 파일이 얼마나 변경됐는지 통계 요약 → CSS 비대화 조기 감지.

### 2-4. 부분 스테이징 (git add -p) — 하나의 파일에 두 가지 변경이 섞인 경우

```
상황: post7_ui.html에 (1) 버그 수정 + (2) 새 컴포넌트 추가가 동시에 들어 있을 때

git add -p widgets/post7_ui.html
→ 각 hunk별로 y/n 선택
→ 버그 수정만 먼저 커밋, 새 컴포넌트는 다음 커밋으로 분리
```

---

## 3. design_ui.md에 추가할 git 운영 섹션 초안

아래 내용을 `design_ui.md` 하단 섹션으로 추가 제안 (실제 수정은 dev 에이전트 담당).

---

### git 운영 표준 (design_ui 자산 관리)

**브랜치 명명 규칙**

| 용도 | 브랜치명 예시 |
|---|---|
| 신규 컴포넌트 개발 | `feat/BH-score-board-v2` |
| CSS 변수 실험 | `exp/css-dark-mode-tokens` |
| 긴급 버그 수정 | `fix/BH-timer-warn-color` |
| 포스트별 UI 패키지 | `post/p8-ui-components` |

**커밋 메시지 형식** (ch5 가이드라인 준용)

```
[컴포넌트] 변경 요약 (50자 이내)

- 변경 이유
- 영향 범위: 어떤 BH_ 클래스·변수에 영향
- QA 점검 항목
```

예시:
```
[BH_progress] 진행바 다크모드 CSS 변수 대응

- light-dark() 함수로 배경색 전환 추가
- 영향 범위: .BH_progress_wrap, .BH_progress_fill
- QA: prefers-color-scheme dark에서 색상 확인 필수
```

**권장 워크플로**

```
main (안정)
  → feat/브랜치 (실험)
    → 완성 후 merge → main
    → 미완성 폐기 → git branch -D
```

**긴급 전환 시 stash 사용 필수** — 미완성 파일을 그냥 checkout하면 변경사항 유실 위험.

---

## 4. 위험·함정

| 함정 | 내용 | 대응 |
|---|---|---|
| `git add .` 습관 | `.~lock.*` 임시 파일·`*.png` 바이너리 등 의도치 않은 파일 포함 | `.gitignore`에 `*.~lock.*`, `*.png`, `node_modules/` 사전 등록 |
| `git commit --amend` 남용 | 이미 push된 커밋을 amend하면 원격 히스토리 충돌 | amend는 로컬 최신 커밋에만 사용. push 후에는 새 커밋 생성 |
| stash 미사용 강제 checkout | Modified 파일이 있을 때 checkout하면 변경사항 유실 또는 충돌 | 브랜치 전환 전 반드시 commit 또는 stash |
| CSS 단일 행 규칙 + git diff | minify된 CSS는 git diff에서 변경 범위 파악이 어려움 | 개발 중에는 멀티라인으로 작업 → 최종 납품 직전에 minify |
| 대용량 파일 커밋 | PNG·SVG 바이너리를 git에 직접 commit하면 저장소 비대화 | `design/` 폴더의 `.png` 파일은 `.gitignore`에 추가 또는 Git LFS 검토 |
| `git reset --hard` 실수 | 커밋하지 않은 작업 전부 삭제 (복구 불가) | 실험 전 반드시 commit 또는 stash 후 사용 |

---

## 협업 약속 자가 점검

| 항목 | 확인 |
|---|---|
| 도박 연상 요소 0건 (BET·JACKPOT·칩 등) | ✅ |
| 결과 화면 면책고지 포함 | ✅ |
| BH_ prefix 네이밍 일관성 | ✅ |
| CSS 단일행 (wpautop 방어) | ✅ |
| 버튼 min-height 44px 이상 | ✅ |
| 커밋 전 `git diff --staged` 검토 | ✅ |
| 실험 브랜치 merge 또는 폐기 완료 후 main 복귀 | ✅ |
| stash list 잔여물 0건 확인 | ✅ |
| `.gitignore`에 PNG·임시파일 등록 여부 확인 | ✅ |
| 커밋 메시지에 영향 범위(BH_ 클래스·변수명) 명시 | ✅ |
