# Pro Git 학습 — game_planner 에이전트 관점

처리 시간: 챕터 5개(ch1·ch2·ch3·ch5·ch7) 분석, 작성 완료.

---

## 1. 핵심 git 명령어 (기획서 버전 관리에 유용한 것)

| 명령어 | 용도 | game_planner 활용 예시 |
|---|---|---|
| `git init` | 저장소 초기화 | `C:\Claude_code\` 이미 적용됨 |
| `git add game_plans/post{N}_game_plan.md` | 파일 추적 시작 | 새 기획서 작성 후 스테이징 |
| `git commit -m "기획서 설명"` | 스냅샷 저장 | "Post7 민화투: 족보 점수 체계 확정" |
| `git log --oneline` | 기획 이력 조회 | 어느 시점에 어떤 결정을 내렸는지 확인 |
| `git diff` | 변경 내용 비교 | 기획서 수정 전후 차이 시각화 |
| `git checkout -b feature/난이도변형` | 브랜치 생성+전환 | 난이도별 변형 기획 독립 분기 |
| `git merge feature/난이도변형` | 브랜치 병합 | 검토 완료된 변형안을 main에 통합 |
| `git tag -a v1.0 -m "최초 승인본"` | 버전 태그 | lead 승인 시점을 태그로 고정 |
| `git stash` | 임시 보관 | 긴급 수정 중 기존 작업 임시 저장 |
| `git stash apply` | 임시 보관 복원 | 긴급 작업 후 원래 기획 작업 재개 |
| `git reset HEAD~1` | 커밋 되돌리기 | 잘못된 기획 결정 직전으로 복귀 |
| `git log --since="2weeks"` | 기간 기반 조회 | 최근 2주간 기획 변경 이력 확인 |

---

## 2. 기획서 버전 관리 워크플로우

### 기획 변경 단위 (커밋 1개 = 결정 1건)

Pro Git ch5는 "각 커밋은 논리적으로 구분되는 변경 단위"라고 명시한다. 기획서에도 동일 원칙을 적용한다.

```
[좋은 커밋 예시 — 결정 1건씩]
feat: Post7 민화투 족보 6종 점수 확정
fix: Post8 스트룹 문항 수 15개→20개로 조정
docs: Post5 기억력 카드 UX 흐름도 추가
refactor: N-Back 난이도 기준 쉬움/보통/어려움 재정의

[나쁜 커밋 예시 — 여러 결정 혼합]
update: 기획서 수정  (무슨 결정인지 불명)
```

### 기획 분기 다이어그램 (난이도별 변형 관리)

```
main
  |
  |-- [tag: v1.0] Post7 민화투 기획서 최초 승인본
  |
  |-- feature/Post7-easy-mode-variant
  |     |
  |     |-- 쉬움 모드: AI 무작위 + 힌트 설계 실험
  |     |-- 피드백 메시지 조정
  |
  +-- merge → main [승인 후]
  |
  |-- feature/Post9-relax-game
        |-- 이완 집중 게임 기획 독립 작업
```

### 롤백 시나리오

| 상황 | 명령어 | 결과 |
|---|---|---|
| 커밋 직전 — stage 취소 | `git reset HEAD game_plans/post7_game_plan.md` | 수정 내용 유지, stage 해제 |
| 커밋 직후 — 마지막 커밋 되돌리기 | `git reset HEAD~1` | 커밋 취소, 수정 내용 유지 |
| 승인된 버전으로 완전 복귀 | `git checkout v1.0 -- game_plans/post7_game_plan.md` | 태그 시점 파일 복원 |
| 2주 전 기획서 확인 (읽기) | `git show master@{14.days.ago}:game_plans/post7_game_plan.md` | 이전 내용 조회 |

### 기획서 변경 이력 추적 예시

```
$ git log --oneline --follow game_plans/post7_game_plan.md

a3f9c12  feat: 족보별 보너스 점수 체계 확정 (+3/+5)
b7e0d4a  fix: 고도리 조건 2.4.8월로 수정 (8월 달광 제외)
c1a2f8b  docs: 민화투 UX 흐름도 v1.3 추가
d5f3e9a  init: Post7 민화투 기획서 초안 작성
```

---

## 3. game_planner.md에 추가할 git 운영 섹션 초안

아래는 dev 에이전트가 `game_planner.md`에 직접 반영할 수 있는 마크다운 블록이다.

---

```markdown
## git 운영 규칙 — 기획서 버전 관리 (★ 신설)

### 기획서 파일 경로
`C:\Claude_code\game_plans\post{N}_game_plan.md`

### 커밋 타이밍 (언제 커밋하는가)
| 시점 | 커밋 메시지 예시 |
|---|---|
| 기획서 초안 완성 | `feat: Post{N} {게임명} 기획서 초안` |
| lead 검토 의견 반영 | `fix: {수정 항목 요약}` |
| lead 최종 승인 | `release: Post{N} 기획서 승인 — tag v{N}.0` |
| 구현 중 기획 변경 | `fix: game 피드백 반영 — {변경 항목}` |

### 난이도 변형 브랜치 운영
- 난이도별 대안 기획이 필요할 때: `git checkout -b feature/Post{N}-난이도변형`
- 검토 완료 후 main 반영: `git merge feature/Post{N}-난이도변형`
- 폐기: `git branch -d feature/Post{N}-난이도변형`

### 승인본 태그 규칙
- lead 승인 직후: `git tag -a vN.0 -m "Post{N} {게임명} 기획서 승인"`
- 이전 승인본 조회: `git show vN.0:game_plans/post{N}_game_plan.md`

### 긴급 수정 절차 (다른 포스트 기획 중에 기존 기획 수정 요청 시)
```bash
git stash                          # 현재 작업 임시 보관
git checkout game_plans/post{N}_game_plan.md  # 해당 기획서 수정
git add game_plans/post{N}_game_plan.md
git commit -m "fix: 긴급 수정 — {사유}"
git stash apply                    # 원래 작업 복원
```

### 커밋 메시지 규칙 (50자 이내 요약 + 상세 설명)
- `feat:` 신규 기획 항목 추가
- `fix:` 기존 기획 수정
- `docs:` 다이어그램·표 등 문서 추가
- `refactor:` 구조 재정리 (내용 변경 없음)
- `release:` 승인 완료 태그 시점

### 협업 약속 자가 점검표

| 항목 | 기준 | 확인 |
|---|---|---|
| 커밋 단위 | 결정 1건 = 커밋 1개 | [ ] |
| 메시지 명확성 | 50자 이내, 무슨 결정인지 명시 | [ ] |
| 승인 태그 부착 | lead 승인 후 즉시 tag 생성 | [ ] |
| 브랜치 정리 | merge 완료 후 feature 브랜치 삭제 | [ ] |
| 긴급 수정 | stash 활용, 작업 맥락 보존 | [ ] |
```

---

## 4. 위험·함정

| 위험 | 상황 | 예방 방법 |
|---|---|---|
| `git commit --amend` 남용 | 공유된 커밋을 amend하면 히스토리 불일치 | amend는 push 전, 로컬 커밋에만 사용 |
| `git reset --hard` 실수 | 커밋되지 않은 기획 내용 영구 손실 | 작업 중 수시로 commit. hard reset 전 stash |
| 기획서 .gitignore 누락 | 임시 파일이 함께 커밋됨 | `.gitignore`에 `*.tmp`, `~$*` 추가 |
| 브랜치 미정리 | feature 브랜치 누적으로 이력 혼잡 | merge 후 즉시 `git branch -d` |
| 대용량 바이너리 커밋 | 게임 위젯 PNG·이미지 직접 커밋 | 이미지는 WP 미디어 라이브러리로만 관리, git 추적 제외 |
| 커밋 메시지 모호 | "기획서 수정" 반복 → 이력 가독성 0 | 메시지에 게임명·변경 항목 반드시 명시 |

---

### 참고: brain_health 프로젝트 현재 git 상태

`C:\Claude_code\` 저장소는 이미 git init된 상태(main 브랜치 존재). game_plans/ 폴더의 기획서 파일을 `git add` + `git commit`하는 것만으로 즉시 버전 관리 시작 가능.

```bash
git add game_plans/
git commit -m "feat: game_planner 기획서 git 버전 관리 도입"
```
