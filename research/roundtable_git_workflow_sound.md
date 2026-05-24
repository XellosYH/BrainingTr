# 라운드테이블 의견서 — sound 에이전트 관점
# 화투게임 git 관리 + 게임 개발 협업 워크플로우

**페르소나**: sound 에이전트 v1.5
**처리 시간**: progit_sound.md(155줄) + sound.md(898줄) 순차 Read 완료. 총 소요 약 1분.
**작성일**: 2026-05-25

---

## §주제1 의견 — 화투게임 git 관리: 효과음 관점

### 핵심 전제: sound 산출물은 git 친화적 텍스트 자산이다

BH Sound Module은 순수 JavaScript 텍스트다. `.mp3`, `.ogg` 같은 바이너리 오디오 파일이 0건이라는 점이 sound 영역의 가장 중요한 git 특성이다. 주파수 값 하나(`o.frequency.value = 800`), gain 수치 하나(`g.gain.setValueAtTime(0.15, ...)`)가 모두 `git diff`로 정확히 추적된다. 사운드 디자인 결정의 전 이력이 숫자 수준까지 보존된다는 의미다.

### commit 단위 원칙: 효과음 1종 = 커밋 1개

6종(클릭·정답·오답·완료·비프·리셋)이든 11종(민화투 확장)이든, commit 단위는 효과음 함수 1종 추가·수정으로 유지해야 한다. 여러 함수를 묶어 "효과음 수정"으로 커밋하면 롤백 단위가 불명확해진다. 형식은 아래를 표준으로 제안한다.

```
feat(sound): BH_playJokbo 족보달성음 신규 추가
tune(sound): BH_playCardMatch gain 0.18→0.2 상향 — QA 피드백 반영
fix(sound): BH_duckOtherSounds ducking 페이드 100ms 누락 수정
```

파라미터 변경 시 이전값→이후값을 메시지에 명시하는 것이 핵심이다. 이 이력이 누적되면 "어떤 수치에서 최적 사운드가 나왔는가"를 git log만으로 추적할 수 있는 학습 자산이 된다.

### 파라미터 튜닝 이력의 학습 자산 가치

음량, 주파수, envelope 수치는 주관적 청각 판단이 개입되므로 A/B 실험이 필수다. 브랜치를 활용한 패턴을 제안한다.

```
main
 ├── tune-jokbo-v1: 도미솔도 523→659→784→1047Hz
 └── tune-jokbo-v2: 5음 G4→E5 팡파레 392→440→494→523→659Hz
```

두 브랜치를 각각 게임에 임시 삽입해 청취 비교 후 채택 브랜치만 main에 merge한다. 미채택 브랜치도 삭제 전에 태그를 달아두면 "왜 이 주파수를 버렸는가"라는 설계 판단이 이력으로 남는다. 이것이 단순 버전 관리를 넘어선 사운드 디자인 지식 베이스다.

### 정본 파일 위치 문제: post7_sound_module.js vs 인라인 통합

현재 `widgets/post7_sound_module.js`와 `widgets/post6_widget.html` 인라인 두 곳에 sound 코드가 존재하는 상황이다. sound 관점의 명확한 입장은 다음과 같다.

**sound의 정본은 `widgets/post{N}_sound_module.js`** 이다.

근거: 인라인 통합본은 wpautop minify 결과물이므로 가독성이 없고, git diff가 1행 변경으로만 표시된다. 주파수 수치 변경이 diff에서 보이지 않으면 파라미터 튜닝 이력 추적이 불가능하다. 원본 주석 포함 파일에서 수정 후 minify해서 game에 전달하는 흐름이 올바른 방향이다.

따라서 `.gitignore`에는 WP 업로드 전 임시 base64 청크(`fix_b64_*.js`) 패턴만 추가하고, `post{N}_sound_module.js`는 반드시 git 추적 대상으로 유지해야 한다.

WP 업로드 직전에는 태그를 생성해 롤백 기준점을 명시한다.

```
git tag -a sound-v1.5-post7 -m "Post #7 민화투 사운드 모듈 WP 업로드"
```

---

## §주제2 의견 — 앞으로 게임 개발 협업 워크플로우

### 공통 sound library: BH_sound_common.js

클릭음·정답음·오답음·완료음·카운트다운·리셋음 6종은 게임 유형에 무관하게 모든 위젯에서 재사용 가능하다. 이를 별도 공통 파일로 분리해 git 관리할 것을 제안한다.

```
widgets/
  BH_sound_common.js       -- 6종 기본 모듈 (game 무관 공통)
  post7_sound_module.js    -- 민화투 전용 확장 (+5종)
  post8_sound_module.js    -- 다음 게임 전용 확장
```

새 게임을 만들 때 sound가 납품하는 블록은 `BH_sound_common.js` 내용 + 해당 게임 전용 확장 함수 합산 형태다. game 에이전트는 두 파일의 합산 블록을 받아 위젯에 인라인 삽입한다.

### sound -> game 핸드오프 commit 단위

sound가 game에 전달을 완료한 시점을 별도 커밋으로 명시하는 것을 제안한다.

```
handoff(sound→game): Post #8 사운드 모듈 v1.0 전달 완료
-- BH_sound_common.js v1.5 + post8_sound_module.js v1.0
-- 효과음 목록: S01-S11 (11종)
-- game은 BH_queueSound() 인터페이스로만 호출할 것
```

이 커밋은 sound 책임 범위 종료를 명시하는 경계점이 된다. 이후 game이 위젯에 통합한 결과물에서 사운드 문제가 발생하면, 이 커밋 이전 이력은 sound 책임, 이후는 game 책임 범위로 명확히 구분할 수 있다.

### 검증 게이트: 음량 자동 점검 가능성

완전 자동화는 현실적으로 어렵다. Web Audio API는 브라우저 런타임 환경이므로 git push 전 Node.js CLI에서 음량 수치를 직접 측정할 수 없다. 단, JS 소스 정적 분석으로 대안적 게이트를 구성할 수 있다.

```
push 전 자동 점검 항목 (정적 분석 가능):
1. gain 값 0.3 초과 여부 검출 (피크 과부하 방지)
2. BH_SoundMuted 체크 누락 함수 grep
3. new AudioContext() 직접 호출 grep (BH_getAC() 미경유)
4. try-catch 미래핑 함수 grep
```

이 4개 항목은 파일 텍스트 grep으로 검증 가능하므로 git pre-commit hook에 쉘 스크립트로 등록할 수 있다. 실제 음량 측정은 QA 에이전트의 브라우저 검수 단계에 위임한다.

### 다른 에이전트에게 요구하는 인터페이스 약속 3개

sound 모듈 내부 구조(함수명, 파라미터 수치, 우선순위 큐 구현)는 언제든 변경될 수 있다. game 에이전트가 내부 함수를 직접 호출하면 sound 내부 변경이 game에 연쇄 영향을 준다. 이를 방지하기 위해 아래 3개 인터페이스 약속을 제안한다.

**약속 1 — 호출 인터페이스 단일화**

game은 개별 `BH_play*()` 함수를 직접 호출하지 않는다. 반드시 `BH_queueSound(type, fn)` 통해서만 호출한다. `type` 문자열('click', 'correct', 'jokbo' 등)만 알면 sound 내부를 몰라도 된다.

```javascript
// game이 사용하는 유일한 인터페이스
BH_queueSound('jokbo', function(done) { BH_playJokbo(done); });
BH_queueSound('match', function(done) { BH_playCardMatch(done); });
```

**약속 2 — 이벤트 트리거 시점 명시**

game_planner가 기획서에 "이벤트 X 발생 시 효과음 Y 재생"을 명시하면, sound가 해당 매핑을 sound_module.js에 주석으로 기록하고, game은 그 매핑에 따라 이벤트 핸들러에 `BH_queueSound()` 호출을 삽입한다. 매핑 결정권은 sound에 있다.

**약속 3 — TTS/나레이션은 sound 범위 외, 별도 커밋 영역**

향후 TTS 기능이 추가될 경우, TTS 코드는 반드시 별도 파일(`BH_tts_module.js`)과 별도 commit prefix(`tts:`)로 분리한다. sound 모듈과 같은 파일·같은 커밋에 섞지 않는다. TTS 에이전트가 별도 지정되거나 sound 범위 확장이 명시적으로 결정될 때까지, sound는 TTS 코드를 작성하거나 수정하지 않는다.

### BGM은 sound 범위 내이나 독립 파일 분리를 권장

현재 sound.md v1.3~v1.5에 BGM(배경음악) 코드가 포함되어 있다. BGM은 효과음과 달리 게임 내내 지속 재생되므로 game의 FSM 상태와 긴밀하게 연동된다. 이 연동 코드가 sound_module.js 안에 혼재하면 game 에이전트가 수정해야 할 범위가 불명확해진다. `BH_startBGM()`, `BH_stopBGM()`, `BH_crossfadeBGM()` 함수를 별도 `BH_bgm_module.js`로 분리하고 game이 이 파일만 FSM과 연동하도록 구조를 명확히 하는 것이 장기적으로 더 건강하다. 단, 이 분리는 현재 즉시 실행할 사항이 아니며 다음 신규 게임 개발 착수 시 적용을 권장한다.

---

## §다른 에이전트에게 요청

**game 에이전트에게**: `BH_queueSound()` 인터페이스 약속을 위젯 코드에 반영해 줄 것. 현재 `post7_widget.html` 안에 `BH_playCardMatch()` 직접 호출이 있다면 `BH_queueSound('match', ...)` 패턴으로 전환을 검토해 달라.

**game_planner 에이전트에게**: 기획서 [효과음 매핑] 섹션에 이벤트 이름(문자열 key)을 명시해 줄 것. sound가 우선순위 큐 type 값을 기획서 key와 일치시킬 수 있도록. 예: "족보 달성 이벤트 → sound key: `jokbo`".

**qa 에이전트에게**: 효과음 QA 체크리스트에 "뮤트 상태에서 어떤 사운드도 재생되지 않는가" 항목이 포함되어 있는지 확인 바람. 또한 각 효과음이 사용자 클릭 이벤트 핸들러 내에서만 최초 호출되는지(NotAllowedError 방지) 브라우저 콘솔 오류 0건 확인을 QA 기준에 포함해 줄 것.

---

## §협업 약속 자가 점검

| 항목 | sound 관점 기준 | 확인 |
|---|---|---|
| 정본 파일 | `widgets/post{N}_sound_module.js` git 추적 대상 유지 | |
| commit 단위 | 효과음 함수 1종 = 커밋 1개 | |
| commit 메시지 | `feat/tune/fix(sound): 함수명 변경내용 이전값→이후값` | |
| WP 업로드 태그 | PUT 직전 `git tag -a sound-vX.X-postN` 생성 | |
| 인터페이스 약속 | game은 `BH_queueSound()` 통해서만 호출 | |
| TTS 분리 | TTS 코드는 sound 파일·커밋과 절대 혼용 금지 | |
| 음량 정적 게이트 | gain > 0.3 grep + BH_SoundMuted 누락 grep (pre-commit) | |
| bgm 분리 계획 | 차기 게임 착수 시 `BH_bgm_module.js` 분리 적용 | |
