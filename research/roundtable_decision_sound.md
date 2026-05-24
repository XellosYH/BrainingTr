# 라운드테이블 2차 결정 표명 — sound 에이전트

**페르소나**: sound 에이전트 v1.5
**처리 시간**: 5종 의견서 순차 Read 후 작성 완료 (약 3분)
**작성일**: 2026-05-25

---

## Q1. 위젯 파일 구조

**1순위: B — 개발용 분리본 + 납품용 통합 minify 2단계**

**근거**: game 의견서는 "인라인 통합"을 현실적이라 했고, design_ui는 `post{N}_ui_dev.html` 개발용 원본 분리를 제안했다. sound도 같은 구조적 문제에 직면한다. `widgets/post{N}_sound_module.js`(주석 포함 멀티라인)가 개발·튜닝 정본이고, game에 전달하는 납품 블록은 minify된 인라인 형태다. 이 2단계 흐름이 "파라미터 변경이 git diff에 보인다"는 sound 핵심 요구와 "wpautop 방어를 위한 단일행 납품"이라는 WP 제약을 동시에 만족한다.

C안(완전 분리 `.js` 단독)은 WP `wp:html` 블록이 외부 파일 import를 지원하지 않으므로 최종 납품 형태로 불가능하다. A안(인라인만)은 diff에서 주파수 수치·gain 수치 변경이 1행 더미로 묻혀 추적 불가다.

**자기 영역 영향**: `widgets/post{N}_sound_module.js` 멀티라인 원본을 git 추적 대상으로 유지, minify 결과물은 game 위젯 인라인 통합 시점 커밋에 포함. sound 단독 커밋은 원본 `.js` 파일 기준으로 한다.

---

## Q2. LFS 도입 임계값

**1순위: A — 50포스트/200MB 초과 시 도입**

**근거**: design 의견서가 동일 기준(50포스트/200MB)을 제시했고 근거가 타당하다. sound 산출물은 순수 JavaScript 텍스트이므로 LFS 대상이 아니다. 이 결정은 design과 game의 PNG/HTML 바이너리 누적 속도에 달린 문제다. sound 관점에서 임계값 논쟁보다 "sound 파일은 LFS 대상 외"라는 점만 명확히 하면 충분하다. 50/200MB 기준은 합리적이며 현재 규모에서 즉시 도입 부담이 없다.

**자기 영역 영향**: sound 산출물(`.js` 텍스트)은 LFS 대상 아님. `git lfs track` 패턴에 `*.js` 미포함 확인 필수.

---

## Q3. pre-commit hook 작성 책임

**1순위: B — 단계적 도입**

**근거**: sound는 1차에서 4개 정적 분석 게이트를 제안했다. (1) gain > 0.3 grep, (2) `BH_SoundMuted` 체크 누락, (3) `new AudioContext()` 직접 호출, (4) try-catch 미래핑. 이 4개는 파일 텍스트 grep으로 즉시 구현 가능하며 false-positive가 거의 없다. 그러나 dev 일괄 위임(A안)으로 처음부터 8개 에이전트 규칙을 한꺼번에 hook으로 만들면 유지 비용이 크다.

단계적 도입이 맞다. 1단계로 sound 4개 게이트만 먼저 hook에 추가하고, 다른 에이전트 규칙은 실제 사고 발생 시 순차 추가하는 방식이 현실적이다. design_ui가 제안한 BH_ prefix 검증, wpautop 단일행 검증도 같은 방식으로 순차 추가하면 된다.

**자기 영역 영향**: sound 4개 게이트를 dev에 전달해 hook 등록 요청. 스크립트는 sound가 초안 작성, dev가 `.git/hooks/pre-commit`에 통합.

```bash
# sound gate — pre-commit 추가 대상
grep -rn "gain\.setValueAtTime(0\.[4-9]\|gain\.setValueAtTime([1-9]" widgets/post*_sound_module.js && echo "FAIL: gain > 0.3 초과" && exit 1
grep -rn "function BH_play" widgets/post*_sound_module.js | grep -v "BH_SoundMuted" && echo "FAIL: BH_SoundMuted 체크 누락" && exit 1
grep -rn "new AudioContext\|new webkitAudioContext" widgets/post*_sound_module.js && echo "FAIL: BH_getAC() 미경유 직접 호출" && exit 1
```

---

## Q4. 인터페이스 약속 7건 .md 일괄 반영

**1순위: A — 7건 모두 즉시 일괄 반영**

**근거**: 게임 에이전트 5종이 라운드테이블에서 합의한 인터페이스 약속은 의견서에 이미 기술 완료 상태다. 단계적으로 반영하면 "현행 .md와 합의 내용이 어긋나는 과도기"가 발생한다. 이 과도기에 새 에이전트가 구버전 .md를 읽고 작업하면 사고 재발 위험이 있다. 즉시 반영이 안전하다.

sound.md에 즉시 반영 필요한 항목: `BH_queueSound()` 단일 호출 인터페이스 표준화, BGM GainNode 전역 저장 패턴, 뮤트 상태 localStorage 저장. 이 3개는 sound 도메인 직결이므로 반영 우선도가 높다.

**자기 영역 영향**: 즉시 반영 후 sound.md 버전 bump(v1.5 → v1.6). 스냅샷 및 changelog 갱신은 dev 에이전트에 위임.

---

## Q5. 태그 명명 규칙 통일

**1순위: A — 영역별 prefix 표준 통일**

**근거**: 1차 의견서에서 sound는 `sound-v1.5-post7` 형식을 제안했다. game은 `deploy:` commit 방식, design은 `hwatu-gwang-complete` / `design-p7-v1` 형식을 제안했다. 에이전트마다 prefix가 다르면 `git tag -l`에서 어떤 태그가 어느 에이전트 산출물인지 파악이 어렵다.

통일 안을 제안한다:

| 에이전트 | 태그 prefix | 예시 |
|---|---|---|
| game | `game/` | `game/post7-v1.0` |
| design | `design/` | `design/post7-v1` |
| design_ui | `ui/` | `ui/post7-v1` |
| sound | `sound/` | `sound/post7-v1.5` |
| game_planner | `plan/` | `plan/post7-v1.0` |
| 릴리즈(WP 업로드) | `release/` | `release/post7-2026-05-25` |

영역별 prefix로 구분하면 `git tag -l "sound/*"` 명령으로 sound 관련 태그만 필터링 가능하다. B안(release 태그만 통일)은 개발 중 이정표 추적이 어렵다.

**자기 영역 영향**: 기존 `sound-v1.5-post7` 형식을 `sound/post7-v1.5`로 변경. WP PUT 직전 태그 생성 규칙은 유지.

---

## 협업 약속 자가 점검

| 항목 | 기준 | 상태 |
|---|---|---|
| 도박 연상 표현 0건 | 잭팟·코인·칩·카지노 표현 없음 | 확인 |
| 정체성 유지 | 두뇌 트레이닝 효과음 전담, TTS 제외 | 확인 |
| 자기 영역 관점만 표명 | sound 도메인 영향 중심으로만 근거 기술 | 확인 |
| 타 에이전트 의견 대변 금지 | 타 에이전트 의견은 교차 참조 인용만, 대변 없음 | 확인 |
| AudioContext 싱글톤 준수 | `BH_getAC()` 경유 원칙 유지 | 확인 |
| 뮤트 체크 표준 | 모든 재생 함수 첫 줄 필수 | 확인 |
| Q1·Q3 근거 강화 | sound 핵심 도메인으로 상세 근거 제시 | 확인 |
| 처리 시간 명시 | 5종 의견서 Read 후 약 3분 | 확인 |
