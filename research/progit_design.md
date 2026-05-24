# Pro Git 학습 산출물 — design 에이전트 관점
**작성일**: 2026-05-25
**버전**: v1.0
**처리 소요 시간**: 약 35분 (5개 챕터 Read + 흡수 + 산출물 작성)

---

## 협업 약속 자가 점검

| 항목 | 상태 | 비고 |
|---|---|---|
| 본 작업이 design 본연 영역인가 | ✅ | git 운영 지식 학습·정리 — design 페르소나 |
| design.md 직접 수정했는가 | ✅ 금지 준수 | §3은 "초안 블록"으로 별도 산출 |
| 타 프로젝트 식별자 0건 | ✅ | brain_health_1.0 전용 |
| 도박 연상 표현 0건 | ✅ | 화투 카드 = 인지 강화 훈련 도구 자산 |
| 의료 단정 표현 0건 | ✅ | 해당 없음 |
| 4원칙 — 단순함 우선 적용 | ✅ | 요청 외 기능 추가 없음 |
| 4원칙 — 외과적 변경 | ✅ | 요청한 4섹션만 산출 |

---

## §1. 핵심 git 명령어 (design 작업 기준)

### 일상 작업 명령어

```powershell
# 상태 확인 (작업 전 필수)
git status
git status -s                        # 단축 출력

# 자산 추가 및 커밋
git add design/p7c01_body.png        # 특정 파일만 추가 (git add -A 금지 — CLAUDE.md 룰)
git add design/                      # design 폴더 전체
git commit -m "design: Post #7 카드 이미지 3장 body/og 버전 추가"

# 히스토리 조회 (이미지 파일 변경 이력)
git log --oneline --name-status -- design/   # design 폴더 변경 이력
git log --oneline -- design/p7c01_body.png   # 특정 파일 이력
git log -p -- design/p7c01_body.png          # diff 포함 (바이너리는 의미 없음)

# 태그 — 디자인 마일스톤 기록
git tag -a design-v1.0 -m "Post #7 카드 이미지 완성 (body+og 2버전)"
git push origin --tags

# 리모트 동기화
git fetch origin
git pull origin main
git push origin main

# 롤백 — 잘못된 PNG 커밋 되돌리기
git checkout HEAD -- design/p7c01_body.png   # 마지막 커밋 버전으로 복원
git reset HEAD design/p7c01_body.png         # Staging 취소

# 바이너리 파일 히스토리 비교 (텍스트 diff 불가 — 파일명으로 변경 확인)
git log --name-status --oneline | grep "design/"

# Stash — 작업 중 긴급 전환 시
git stash
git stash pop
```

### 태그 명명 규칙 (design 전용)

```
형식: design-p{N}-v{버전}
예시:
  design-p7-v1        # Post #7 카드 이미지 1차 납품
  design-p7-v2        # 수정본
  hwatu-48-complete   # 화투 SVG 48장 완성 마일스톤
  infographic-set-01  # 뇌건강 인포그래픽 1세트 완성
```

### .gitignore design 관련 항목

```gitignore
# design 임시 파일
design/_tmp*/
design/*.bak
design/*.bak-pre-*
*_render_cache*/
html2canvas_tmp*/

# SVG → PNG 변환 중간 산출물
design/*_draft.svg
design/*_working.svg

# OS 생성 파일
Thumbs.db
.DS_Store
```

---

## §2. design 영역 워크플로 (카드 PNG body/og 2버전 제작·납품·롤백)

### 제작 단계 git 활용 절차

```
[1단계] 작업 시작 전 상태 확인
  git status                          # 이전 작업 잔여물 없는지 확인
  git pull origin main                # 최신 상태 동기화

[2단계] SVG 초안 작성 → 중간 저장
  # SVG 파일은 텍스트 → diff 가능 → 의미 있는 중간 커밋 가능
  git add design/p7c01_body.svg
  git commit -m "design: Post #7 c01 body SVG 초안 — 뇌 해마 구조 인포그래픽"

[3단계] PNG export (html2canvas or 직접 캡처)
  # PNG 생성 후 즉시 커밋 (바이너리지만 시점 기록 중요)
  git add design/p7c01_body.png design/p7c01_og.png
  git commit -m "design: Post #7 c01 body.png(1200×630) + og.png(1200×630) export"

[4단계] 3장 세트 완성 후 태그
  git add design/p7c02_body.png design/p7c02_og.png
  git add design/p7c03_body.png design/p7c03_og.png
  git commit -m "design: Post #7 카드 이미지 3장 세트 완성 (c01~c03 body+og)"
  git tag -a design-p7-v1 -m "Post #7 카드 이미지 v1 납품"

[5단계] dev에 납품 — 파일 경로 + 미디어 ID 전달
  # 납품 시 아래 정보 dev에 명시:
  # - body.png 경로: C:\Claude_code\design\p7c01_body.png
  # - og.png 경로: C:\Claude_code\design\p7c01_og.png
  # - git 태그: design-p7-v1 (롤백 기준점)

[6단계] dev 업로드 후 QA 지적 시 수정
  git checkout design-p7-v1 -- design/p7c01_body.png  # v1 복원
  # 수정 후:
  git add design/p7c01_body.png
  git commit -m "design: Post #7 c01 body.png 수정 — 폰트 크기 18px→22px"
  git tag -a design-p7-v2 -m "Post #7 카드 이미지 v2 (폰트 보정)"
```

### 롤백 시나리오별 절차

| 상황 | 명령어 |
|---|---|
| 마지막 커밋 전으로 단일 파일 복원 | `git checkout HEAD -- design/p7c01_body.png` |
| 특정 태그 시점으로 파일 복원 | `git checkout design-p7-v1 -- design/p7c01_body.png` |
| Staging Area에서 파일 제거 | `git reset HEAD design/p7c01_body.png` |
| 커밋 전체 되돌리기(로컬만) | `git reset --hard HEAD~1` |

### 화투 SVG 48장 git 관리 절차

```
[광 5장 먼저 커밋]
  git add design/hwatu_svg/m01_gwang.svg ... m12_gwang.svg
  git commit -m "design: 화투 광 5장 SVG 완성 (1·3·8·11·12월)"
  git tag -a hwatu-gwang-complete -m "화투 광 5장 완성 — dev 테스트 가능"

[전체 48장 완성 후]
  git add design/hwatu_svg/
  git commit -m "design: 화투 SVG 전체 48장 완성 — 저작권 100% 자체제작"
  git tag -a hwatu-48-complete -m "화투 SVG 48장 완성 (월별 광/조/피2)"
```

---

## §3. design.md 추가용 git 운영 섹션 초안

아래 블록은 dev 에이전트가 다음 세션에서 design.md에 그대로 반영할 초안이다.
design.md의 `# 작업 워크플로우` 섹션 아래에 신규 섹션으로 삽입 권장.

---

### [초안 블록 시작]

## git 버전 관리 운영 룰 (design 자산 전용) ★ v6.37 신설

**배경**: brain_health 저장소(C:\Claude_code\)에 git 도입(2026-05-25). PNG·SVG 바이너리 자산 위주이므로 텍스트 코드 git과 다른 운영 방식 필요.

### 바이너리 자산 커밋 원칙

| 원칙 | 내용 |
|---|---|
| **바이너리 diff 무의미 인지** | PNG·래스터화된 이미지는 git diff가 의미 있는 내용을 보여주지 않음. 커밋 메시지로 변경 내용을 명확히 기록해야 함 |
| **SVG는 텍스트 diff 가능** | SVG 파일은 텍스트 형식 → 의미 있는 diff 가능 → 중간 커밋 적극 활용 |
| **커밋 단위** | 포스트 1개 카드 세트(body+og 전체) 완성 시점에 1커밋. 개별 카드 PNG는 draft 제외 |
| **특정 파일 add 원칙** | `git add -A` 또는 `git add .` 금지. 반드시 `git add design/파일명` 형식으로 특정 |

### 커밋 메시지 표준

```
형식: design: {내용 요약} [{상세}]

예시:
  design: Post #7 카드 이미지 3장 body/og 완성
  design: Post #7 c01 body.png 폰트 크기 수정 (18px→22px)
  design: 화투 SVG 광 5장 완성 — 두뇌 트레이닝 게임 자산
  design: .gitignore design 임시파일 패턴 추가
```

### 태그 운영 (디자인 마일스톤)

```powershell
# 포스트 카드 이미지 납품 시점 태그
git tag -a design-p{N}-v1 -m "Post #{N} 카드 이미지 1차 납품"

# 화투 SVG 세트 완성 태그
git tag -a hwatu-gwang-complete -m "화투 광 5장 완성"
git tag -a hwatu-48-complete    -m "화투 SVG 48장 완성"

# 태그 원격 push 필수 (기본 push에 태그 미포함)
git push origin --tags
```

### .gitignore design 관련 필수 항목

```gitignore
# design 임시·작업중 파일 (커밋 대상 제외)
design/_tmp*/
design/*.bak
design/*.bak-pre-*
*_render_cache*/
html2canvas_tmp*/
design/*_draft.svg
design/*_working.svg
```

### 납품 후 롤백 절차

```powershell
# dev 업로드 후 QA 지적 시 — 특정 태그 시점 파일 복원
git checkout design-p{N}-v1 -- design/p{N}c01_body.png

# 수정 완료 후 새 태그
git tag -a design-p{N}-v2 -m "Post #{N} 카드 이미지 v2 수정본"
git push origin --tags
```

### Git LFS 판단 기준

brain_health 현재 규모(포스트 목표 100개, 카드 3장×2버전 = 약 600개 PNG)에서 LFS 미적용 시 저장소 비대화 위험 있음.

| 기준 | 판단 |
|---|---|
| 현재(2026-05-25): PNG 수십 개, 저장소 ~50MB 이하 | LFS 불필요 — 일반 git 관리 |
| 포스트 50개+ 누적, PNG 300개+ 초과 시 | dev 에이전트와 LFS 적용 검토 트리거 |
| 화투 SVG 97개(48장×2 + 뒷면) | SVG는 텍스트 — LFS 불필요 |

**LFS 적용 기준**: 저장소 크기 200MB 초과 또는 `git push` 속도 현저히 저하 시 → lead 보고 후 dev가 LFS 전환 담당.

### 자가 점검 체크리스트 (design 납품 전)

```
[ ] git status — 불필요한 임시 파일(.bak, _tmp) Staged 없음
[ ] 커밋 메시지 "design: " 접두어 포함
[ ] body.png + og.png 2버전 모두 커밋됨
[ ] 납품 태그 생성 + git push origin --tags 완료
[ ] 라이선스 마커 SVG 포함 확인 (<!-- license: 자체제작/... -->)
```

### [초안 블록 끝]

---

## §4. 위험·함정

### 위험 1. 바이너리 diff 무력화

**현상**: `git diff` 실행 시 PNG 파일은 `Binary files a/design/p7c01_body.png and b/design/p7c01_body.png differ` 만 출력. 변경 내용 파악 불가.

**대응책**:
- 커밋 메시지에 변경 내용 명시 (`"c01 body.png — 배경 흰색으로 전환, 폰트 22px 확대"`)
- SVG 단계에서 중간 커밋 적극 활용 (텍스트 diff 가능)
- 백업 파일명에 시점 명시 (CLAUDE.md `★ 백업 파일명 = 실제 내용 상태 정확 반영` 룰 준수)
- 히스토리 확인: `git log --name-status -- design/` 으로 어떤 파일이 언제 변경됐는지 추적

### 위험 2. LFS 미적용 시 저장소 비대화

**현상**: PNG 수백 개 누적 → `.git/objects/` 폴더 수백 MB → `git clone` 느려짐, GitHub 100MB 파일 제한 초과 위험.

**대응책**:
- 현재(포스트 10개 미만): 일반 git 관리 유지
- 포스트 50개 초과 시점에 dev와 `git lfs track "design/*.png"` 도입 검토
- `git lfs` 도입 전: 저장소 크기 정기 점검 `git count-objects -vH`

### 위험 3. Edit 툴 수정 SVG에 NUL 패딩

**현상**: Edit 툴로 SVG 수정 후 파일에 NUL 바이트(`\x00`) 패딩이 발생할 수 있음. git은 이를 정상 변경으로 기록하지만 브라우저/렌더러가 SVG 파싱 실패.

**대응책**:
- 래스터화(PNG export) 전 NUL strip 1회 검증 (design.md §산출물 검증 표 룰)
- mount 캐시 지연 의심 시: `/tmp` 로컬 복사 후 렌더 검증 (CLAUDE.md §산출물 검증 표 룰)
- git 상태 확인: NUL 패딩된 SVG가 커밋되면 이후 렌더 실패 → 해당 커밋 `git revert` 또는 `git checkout HEAD~1 -- design/파일.svg`

### 위험 4. 임시 파일 커밋 사고

**현상**: `git add design/` 으로 임시 파일(_tmp, .bak, html2canvas 캐시)까지 커밋 → 저장소 오염.

**대응책**:
- `.gitignore`에 패턴 등록 선행 (§3 초안 블록 참조)
- `git status -s`로 커밋 전 전체 확인
- `git add -A` / `git add .` 절대 금지 (CLAUDE.md §핵심 룰 준수)

### 위험 5. 잘못된 featured_media 커밋 이후 이미지 혼용

**현상**: body.png를 OG 필드에, og.png를 본문에 잘못 배치한 상태로 dev가 WP 업로드 완료 → git 히스토리에는 파일명 정상이지만 WP 내 배치 오류.

**대응책**:
- 납품 시 dev에게 `body` / `og` 용도 명시 필수 (파일명 suffix가 의도 표시)
- WP 업로드 후 QA가 `featured_media` ID와 본문 figure mediaId 교차 확인 (CLAUDE.md §WP featured_media 렌더링 위치 룰)
- 오배치 발견 시 WP REST PATCH로 교체 (git 이력과 무관)

### 위험 6. Cowork에서 git 실행 금지

**현상**: Linux 샌드박스(Cowork)에서 git 실행 시 `.git/index.lock` NTFS 마운트 권한 문제로 연속 명령 불가.

**대응책**: design 에이전트가 Claude Code(Windows/PowerShell)에서 git 명령 실행. Cowork bash에서 git 금지 (CLAUDE.md §git 운영 룰 준수).

---

*산출물 저장 경로: `C:\Claude_code\research\progit_design.md`*
*참조 입력 파일: ch1~ch3·ch5·ch7 Pro Git 한국어판*
