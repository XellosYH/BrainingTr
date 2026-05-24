# Pro Git 학습 — sound 에이전트 관점

> 처리 시간: 5개 챕터(ch1~ch7) 동시 Read 완료. 총 소요 약 2분.

---

## 1. 핵심 git 명령어 (사운드 모듈 관리에 유용한 것)

| 명령어 | 용도 | sound 모듈 적용 예 |
|---|---|---|
| `git init` | 저장소 초기화 | `widgets/` 디렉토리를 git 관리 대상으로 선언 시 1회 실행 |
| `git add <file>` | 스테이징 | `git add widgets/post8_sound_module.js` — 파일 단위 정밀 추가 |
| `git commit -m "msg"` | 커밋 | "feat: BH_playJokbo 족보달성음 추가" 형태 |
| `git diff` | 변경 내용 확인 | 파라미터 수정 전후 주파수·envelope 수치 diff 확인 |
| `git log --oneline` | 이력 조회 | 효과음 변경 이력 한눈에 파악 |
| `git branch <name>` | 브랜치 생성 | `tune-jokbo-freq` 브랜치에서 주파수 A/B 튜닝 실험 |
| `git checkout -b <name>` | 브랜치 생성+이동 | 새 효과음 실험 즉시 브랜치 분리 |
| `git merge <branch>` | 브랜치 병합 | 실험 브랜치 검증 후 main에 병합 |
| `git stash` | 임시 저장 | 튜닝 중 긴급 버그 수정 시 작업 임시 보관 |
| `git log -S "BH_playJokbo"` | 코드 내 텍스트 검색 | 특정 함수가 변경된 커밋 이력 추적 |
| `git show HEAD~2` | 과거 커밋 조회 | 2커밋 이전 파라미터 값 확인 |
| `git grep "frequency.value"` | 저장소 내 검색 | 모든 주파수 설정 위치 한번에 파악 |

---

## 2. 사운드 튜닝·실험 워크플로우

### 2-A. 효과음 파라미터 A/B 튜닝 브랜치 패턴

사운드 파라미터(주파수·envelope·지속시간) 수치는 청각적 주관이 개입되므로 A/B 비교가 필수다. Pro Git 3장의 토픽 브랜치 개념을 그대로 적용한다.

```
[main]
  |
  |--- git checkout -b tune-jokbo-v1
  |       주파수: 523→659→784→1047 (기존)
  |       커밋: "tune: BH_playJokbo 도미솔도 아르페지오"
  |
  |--- git checkout -b tune-jokbo-v2
          주파수: 392→440→494→523→659 (5음 상행)
          커밋: "tune: BH_playJokbo 5음 G4→E5 팡파레"

# 두 브랜치를 각각 게임에 삽입해 청취 비교 후
# 채택된 브랜치만 main에 merge
git checkout main
git merge tune-jokbo-v2
git branch -d tune-jokbo-v1   # 미채택 브랜치 삭제
```

핵심: 브랜치는 41바이트 파일 하나로 생성 — 실험 비용 0에 가깝다(Pro Git ch3).

### 2-B. 효과음 1종 단위 소규모 커밋

Pro Git ch5 커밋 가이드라인: "각 커밋은 논리적으로 구분되는 Changeset". 사운드 모듈에 직접 적용한다.

```
# 올바른 커밋 단위 (효과음 1종 = 커밋 1개)
git add widgets/post8_sound_module.js
git commit -m "feat(sound): BH_playCardTap S01 800Hz→880Hz 상향"

git commit -m "feat(sound): BH_playNoMatch S05 duration 0.2s→0.3s"

# 잘못된 커밋 단위 (여러 효과음 혼합)
git commit -m "효과음 여러 개 수정"  # 검토·롤백 시 어디를 건드렸는지 불명확
```

커밋 메시지 권장 형식:
```
feat(sound): <함수명> <변경 파라미터> <이전값>→<이후값>
fix(sound): BH_duckOtherSounds 100ms 페이드 누락 수정
refactor(sound): BH_getMasterBus 싱글톤 패턴 적용
```

### 2-C. WP 업로드 전 스냅샷 태그

WP에 업로드한 버전은 되돌리기 어렵다. 업로드 직전 태그를 남겨두면 롤백 기준점이 생긴다.

```
# WP 업로드 직전
git tag -a sound-v1.5-post8 -m "Post #8 화투 사운드 모듈 WP 업로드 버전"

# 이후 파라미터 수정 중 문제 발생 시
git show sound-v1.5-post8:widgets/post8_sound_module.js
# → 태그 시점의 파일 내용 확인 가능
```

### 2-D. git stash — 긴급 버그 수정 시나리오

```
# 시나리오: BH_playJokbo 튜닝 중 Post #8 Mojibake 버그 신고 접수
git stash           # 진행 중인 튜닝 임시 저장
git checkout -b fix-post8-mojibake
# ... 버그 수정 ...
git commit -m "fix: Post #8 한글 Mojibake atob→TextDecoder 교체"
git checkout main
git merge fix-post8-mojibake
git stash apply     # 튜닝 작업 복구
```

---

## 3. sound.md에 추가할 git 운영 섹션 초안

아래 텍스트는 sound.md `## 에이전트 협업 표준` 섹션 이후에 삽입 가능한 초안이다.
sound.md 직접 수정은 이 산출물의 범위 밖이므로 초안만 제시한다.

```markdown
## git 운영 규칙 — sound 모듈 버전 관리

### 커밋 단위 원칙
- 효과음 함수 1종 추가·수정 = 커밋 1개
- 파라미터(주파수·envelope·gain) 변경은 이전값→이후값을 메시지에 명시
- 예: `feat(sound): BH_playJokbo 마지막음 gain 0.2→0.25 강조`

### 브랜치 실험 패턴
- 파라미터 A/B 튜닝: `tune-<함수명>-v1` / `tune-<함수명>-v2` 브랜치 병렬 생성
- 청취 검증 후 채택 브랜치만 main merge, 미채택 삭제
- 브랜치 생성 비용 없음 — 실험 주저하지 말 것

### WP 업로드 태그
- WP PUT 직전: `git tag -a sound-vX.X-postN -m "Post #N WP 업로드"`
- 태그 = 롤백 기준점. QA 실패 시 태그 시점 파일 즉시 복원 가능

### .gitignore 권장
widgets/*.html 중 minify 전 원본이 별도 존재하면 아래 추가:
  *_raw.js        # minify 전 원본 (로컬 작업용, 업로드 금지)
  *.map           # source map
```

---

## 4. 위험·함정

| 함정 | 발생 상황 | 대응 |
|---|---|---|
| **minify 파일 diff 가독성 저하** | JS를 1행 minify 상태로 커밋 시 `git diff`가 1행 변경으로 표시 → 수치 변경 내용 파악 불가 | minify 전 원본(주석 포함)도 별도 파일로 관리. 원본에서 수정 후 minify → 커밋 |
| **대용량 base64 청크 커밋** | BH Sound Module을 base64로 WP에 삽입한 경우, 청크 파일을 git에 추가하면 저장소 비대화 | `.gitignore`에 `fix_b64_*.js` 패턴 추가. 청크는 임시 파일로 취급 |
| **force push 금지** | 실험 브랜치를 remote에 push 후 rebase → force push 필요 상황 | main 브랜치 force push 절대 금지. 실험 브랜치에 한해 `git push -f` 허용, 단 단독 작업 시만 |
| **AudioContext 상태와 git 버전 혼동** | sound 모듈 버전과 WP에 실제 업로드된 버전이 다를 때 디버깅 혼란 | 업로드 완료 즉시 태그. "WP에 있는 것 = 태그" 원칙 유지 |
| **wpautop 변환 후 git diff 오염** | WP GET으로 가져온 콘텐츠에 `<br>` 삽입 → 로컬 파일과 diff 폭발 | GET 원본을 `_wp_raw.js`로 저장 후 비교. git에는 로컬 minify본만 관리 |

---

## 협업 약속 자가 점검표

| 항목 | 기준 | 확인 |
|---|---|---|
| 커밋 단위 | 효과음 1종 = 커밋 1개 | |
| 커밋 메시지 | `feat/fix/refactor(sound): 함수명 변경내용` | |
| 실험 브랜치 | 튜닝 실험은 반드시 별도 브랜치 | |
| WP 업로드 태그 | PUT 직전 태그 생성 완료 | |
| minify 원본 보존 | 주석 포함 원본 파일 별도 관리 | |
| .gitignore 적용 | base64 청크·임시 파일 제외 확인 | |
| force push | main 브랜치 force push 0건 | |
