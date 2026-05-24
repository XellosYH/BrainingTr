# Pro Git 학습 — game 에이전트 관점

## 협업 약속 자가 점검

| # | 약속 | 점검 결과 |
|---|---|---|
| 1 | 본연 주인인 작업만 수행 (game 에이전트 = HTML/CSS/JS 위젯 코드) | ✅ |
| 2 | 산출물 raw data 길이·내용 보존 (dev 에이전트에게 1바이트도 수정 없이 전달) | ✅ |
| 3 | lead 도구 실행 결과 사후 검증 발주 준비 | ✅ |
| 4 | game.md 직접 수정 금지 (dev 에이전트 위임 영역) | ✅ |
| 5 | 도박·사행성 표현 0건 | ✅ |
| 6 | BH_ 네임스페이스 준수 | ✅ |
| 7 | 위젯 파일 단일 정본 룰 준수 (버전 suffix 금지) | ✅ |
| 8 | 전용 함수 재사용 원칙 준수 (모달 display 직접 조작 금지) | ✅ |

---

## 1. 핵심 git 명령어 (위젯 개발에 직접 쓰는 것 위주)

| 명령어 | 용도 | game 영역 적용 예시 |
|---|---|---|
| `git status` | 수정·스테이지 상태 확인 | 위젯 파일 변경 여부 확인 |
| `git diff` | 작업 트리 vs 스테이지 차이 | CSS/JS 변경 내용 사전 검토 |
| `git diff --staged` | 스테이지 vs 마지막 커밋 차이 | PUT 전 최종 변경 확인 |
| `git add widgets/post{N}_widget.html` | 특정 파일 스테이지 등록 | 정본 위젯 파일만 선택적 스테이지 |
| `git commit -m "..."` | 스냅샷 저장 | `"fix: post7 민화투 난이도 모달 display 버그"` |
| `git log --oneline` | 커밋 이력 한 줄 요약 | 위젯 버전 이력 빠른 확인 |
| `git log -p widgets/post7_widget.html` | 특정 파일 변경 diff 이력 | 위젯 파일 변경 전체 추적 |
| `git checkout -- widgets/post7_widget.html` | 작업 트리 변경 취소 | 실험 실패 시 마지막 커밋 상태로 복원 |
| `git reset HEAD widgets/post7_widget.html` | 스테이지 취소 (파일 내용 유지) | 잘못 add한 파일 스테이지 해제 |
| `git stash` | 작업 트리 임시 보관 | 긴급 버그 수정 전 진행 중 작업 보관 |
| `git stash pop` | 보관된 작업 복원 | 긴급 수정 완료 후 원래 작업 재개 |
| `git show HEAD:widgets/post7_widget.html` | 특정 커밋의 파일 내용 출력 | minify 전 원본 복원 확인 |
| `git diff HEAD~1 widgets/post7_widget.html` | 이전 커밋과 차이 비교 | WP PUT 전 무엇이 바뀌었는지 확인 |

---

## 2. 위젯 버전 관리 워크플로우 (정본 파일 룰 정합)

### 정본 파일 원칙

```
widgets/post{N}_widget.html  ← 유일한 정본. v1/v5b 같은 suffix 금지.
```

버전 히스토리는 파일명이 아닌 git 커밋으로 관리한다. "어제 버전으로 돌아가고 싶다"면 `git log`로 커밋 SHA 확인 후 해당 시점 파일을 꺼낸다.

### 브랜치 전략 (소규모 단독 작업 기준)

```
main 브랜치
  ↑
  커밋 A: 초기 위젯 완성 (minify 전 개발 버전)
  커밋 B: minify 적용 + WP 업로드 준비 완료
  커밋 C: BH_howPanel 버그 수정
  커밋 D: 난이도 모달 overflow:hidden 수정
```

topic 브랜치는 대규모 리팩터링·새 게임 추가 시에만 생성한다. 단순 버그 수정은 main에 직접 커밋.

### 커밋 단위 기준

| 커밋 하나에 담을 것 | 분리할 것 |
|---|---|
| 단일 버그 수정 | 버그 수정 + 새 기능 동시 |
| minify 적용 (별도 커밋) | 로직 변경 + minify 혼합 |
| WP PUT 전 최종 검증 통과 상태 | 미완성 상태 |

커밋 메시지 형식 (Pro Git Ch5 기준):
```
fix: post7 민화투 BH_restartGame 타이머 누락 수정

BH_restartGame()이 dm.style.display='' 직접 호출로
BH_startAutoTimer() 부수효과 누락 → BH_showDifficultyModal() 경유로 수정.

영향 범위: post7_widget.html JS 블록만. HTML 구조·CSS 무변경.
```
- 첫 줄: 50자 이하, `fix:` / `feat:` / `style:` / `refactor:` prefix
- 빈 줄
- 본문: 무엇을, 왜 바꿨는지 (영향 범위 명시)

### 롤백 절차

```powershell
# 1. 어떤 커밋으로 돌아갈지 확인
git log --oneline widgets/post7_widget.html

# 2. 특정 커밋의 파일만 꺼내기 (작업 트리에 복원, 커밋하지 않음)
git checkout abc1234 -- widgets/post7_widget.html

# 3. 내용 확인 후 커밋
git add widgets/post7_widget.html
git commit -m "revert: post7 위젯 abc1234 시점으로 복원 (BH_modal display 버그)"
```

`git reset --hard` 는 사용하지 않는다. 위 파일 단위 checkout 방식이 안전하다.

### WP PUT 전 체크포인트 커밋

```powershell
# minify 완료 후, WP PUT 직전 커밋
git add widgets/post7_widget.html
git commit -m "build: post7 위젯 minify 완료 — WP PUT 준비"

# WP PUT 성공 확인 후, 결과 기록 커밋 (파일 변경 없어도 메시지로 기록)
git commit --allow-empty -m "deploy: post7 위젯 WP 업로드 완료 (페이지 ID 303)"
```

---

## 3. game.md에 추가할 git 운영 섹션 초안

> dev 에이전트가 game.md에 그대로 반영할 수 있도록 작성한 마크다운 블록.

```markdown
## 🔵 git 운영 룰 — game 에이전트 위젯 파일 관리 (★ 2026-05-25 신설)

**운영 환경**: Windows (Claude Code / PowerShell) 전용. Cowork Linux 샌드박스에서 git 실행 금지.

### 정본 파일 단일화

| 규칙 | 내용 |
|---|---|
| **정본 경로** | `widgets/post{N}_widget.html` 1개만 존재 |
| **suffix 금지** | `_v1`, `_v5b`, `_backup`, `_old` 등 버전 suffix 파일명 금지 |
| **버전 히스토리** | git 커밋으로 관리. 파일명 버전 관리 금지 |
| **minify 버전** | `_wp.html` 구분 파일도 금지 — minify 결과를 같은 파일에 적용 후 커밋 |

### 커밋 타이밍 의무

1. 위젯 초기 완성 (개발 버전) → 커밋
2. minify 적용 완료 → 별도 커밋
3. WP PUT 성공 확인 → `--allow-empty` 커밋으로 배포 기록

### 커밋 메시지 형식

```
{type}: {50자 이하 요약}

{변경 이유·영향 범위}
```

type: `fix` (버그) / `feat` (신규) / `style` (CSS만) / `refactor` / `build` (minify) / `deploy` (WP 업로드)

### 롤백: 파일 단위 복원

```powershell
git checkout {SHA} -- widgets/post{N}_widget.html
git add widgets/post{N}_widget.html
git commit -m "revert: {이유}"
```

`git reset --hard` 사용 금지 — 작업 트리 전체 파괴 위험.
```

---

## 4. 위험·함정 (Pro Git 책에서 명시)

### 절대 금지 — Force Push + Rebase 조합

> "이미 공개 저장소에 Push 한 커밋을 Rebase 하지 마라" — Pro Git Ch3

로컬에서 rebase 후 `--force` push하면, 다른 작업자(dev 에이전트 등)가 이미 pull한 커밋이 사라지고 중복 커밋이 생긴다. brain_health는 단독 운영이지만, 습관적 rebase + force push는 위젯 히스토리를 파괴하므로 금지.

### git reset --hard — 복구 불가 위험

```powershell
# ❌ 금지 — 스테이지 + 작업 트리 모두 삭제
git reset --hard HEAD

# ✅ 안전 — 스테이지만 취소, 파일 내용 보존
git reset HEAD widgets/post7_widget.html
```

### git checkout -- <file> — 작업 내용 영구 삭제

```powershell
# ❌ 신중하게 — 작업 트리 변경 내용 완전 삭제 (git stash 먼저 고려)
git checkout -- widgets/post7_widget.html
```

실행 전 반드시 `git diff`로 버릴 내용 확인. 복구 방법 없음.

### commit --amend — 푸시 후 사용 금지

```powershell
# ❌ 이미 push한 커밋에 amend → force push 필요 → 히스토리 파괴
git commit --amend

# ✅ 새 커밋으로 수정 (안전)
git commit -m "fix: 이전 커밋 누락 항목 추가"
```

### reflog — 실수 후 복구 경로

`git reset --hard` 실수 등 극단적 상황에서 마지막 수단:

```powershell
git reflog              # HEAD가 이전에 가리켰던 커밋 목록
git checkout {SHA}      # 해당 시점으로 이동
```

reflog는 로컬에만 존재. 원격 서버나 다른 기기에서는 사용 불가.

---

처리 시간: Pro Git 5개 챕터 병렬 Read (ch1·ch2·ch3·ch5·ch7) + 산출물 작성 — 총 약 4분.
