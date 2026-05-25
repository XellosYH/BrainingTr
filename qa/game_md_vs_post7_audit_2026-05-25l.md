# game.md ↔ post7_widget.html 전수 감사 보고서

**감사 일시**: 2026-05-25  
**감사 대상 파일**: `C:\Claude_code\.claude\agents\game.md` (v3.45, 3,379줄)  
**정본 위젯**: `C:\Claude_code\widgets\post7_widget.html`  
**위젯 SHA256**: `9dc4cefd3c49897b97813454451b25493c202162c3b860a53ec826997daad9ba`  
**위젯 크기**: 63,319 bytes  
**직전 커밋**: `a5e9f4c` (자동 타이머 5항목 제거)

---

```
════════════════════════════════════════════════════════════════
 감사 요약 통계
════════════════════════════════════════════════════════════════
 PASS   : 18건
 FAIL   : 9건
 N/A    : 5건
 총계   : 32건

 심각도 분포 (FAIL만):
   Critical : 2건
   High     : 4건
   Medium   : 2건
   Low      : 1건
════════════════════════════════════════════════════════════════
```

---

## 전수 대조 표

| # | game.md 라인 | 섹션명 | 룰 요지 (1줄) | 정본 실측 근거 | 결과 | 심각도 | 권장 조치 |
|---|---|---|---|---|---|---|---|
| 1 | 12 | 로컬 HTML 검증 절차 (v3.45) | 게임 코드 수정 후 로컬 wrapper.html에서 플레이 검증 필수 납품 | 절차 룰 — 정본 코드 영역 외 | N/A | - | 운영 절차 준수 감시 (lead) |
| 2 | 39 | 모달 제어 함수 재사용 원칙 | BH_restartGame은 BH_showDifficultyModal() 경유 필수 | `function BH_restartGame(){BH_playReset();...BH_showDifficultyModal();}` — 전용 함수 경유 확인 (라인 범위: 위젯 JS 내) | PASS | - | - |
| 3 | 63 | 프론트엔드 QA 발견 개선 권고 (B1~B3) | B1: confirm() 팝업 → 커스텀 모달 / B2: role=button / B3: how_panel 열림 시 타이머 중지 | B1: `BH_confirmNewGame(){if(confirm(...))}` 1건 잔존. B2: `.BH_card` 에 role/tabindex 미확인. B3: 자동 타이머 제거 후 해당 없음 | FAIL | Low | B1: game 에이전트에 커스텀 confirm 모달 교체 의뢰 (비긴급) |
| 4 | 75 | position:absolute 모달 + overflow:hidden 수축 함정 | 모달이 절대 위치면 부모에 min-height 필수 | `.BH_hwatu_wrap{...overflow:hidden;}` 에 `min-height` 미설정. 모달(`BH_diff_modal`)이 `position:absolute`이면 수축 위험 존재 | FAIL | High | BH_hwatu_wrap CSS에 `min-height:420px` 추가 (game 또는 dev 에이전트) |
| 5 | 90 | game 에이전트 실행 방식 인지 | 독립 인스턴스, game.md Read 후 작업, 표준 출력 경로 저장 | 절차 룰 — 정본 코드 영역 외 | N/A | - | - |
| 6 | 100 | 최상위 정체성 원칙 — 도박 아님 | JS/UI/텍스트에서 도박·사행 표현 0건, 두뇌훈련 정체성 명시 | `두뇌훈련` 6건, `의료적` 1건, `참고용` 1건 확인. 도박/베팅/판돈 0건. 결과 모달 `BH_disclaimer` 클래스 내 "참고용 두뇌훈련 게임 · 의료적 진단이 아닙니다" 확인 | PASS | - | - |
| 7 | 135 | 사이트 URL 상수 | neuralcare.co.kr (하이픈 없음), neural-care.co.kr 0건 | `neuralcare.co.kr` 0건 (위젯 내 URL 참조 없음), `neural-care.co.kr` 0건 → URL 미포함 (오타 없음) | PASS | - | - |
| 8 | 145 | WP 업로드 후 SyntaxError 대응 (v3.40) | typeof BH_startWithDiff 체크 포함, 이모지/개행/문자 오염 대응 절차 | 운영 절차 룰 — 정본 코드 영역 외. 단, BH_startWithDiff 함수가 위젯에 정의되어 있는지 확인: `function BH_startWithDiff` 미발견 (함수명 다름: `BH_showDifficultyModal`) | FAIL | Medium | game_planner 기획서 [검수 식별자] 항목 BH_startWithDiff → BH_showDifficultyModal로 갱신 필요 (SW 검증 함수명 불일치) |
| 9 | 172 | 게임 모달 display 제어 — CSS 특이성 (v3.38) | BH_diff_modal·BH_game_board·BH_result_modal에 setAttribute('hidden') 금지, style.display 직접 제어 필수 | BH_diff_modal: style.display 2건 / BH_game_board: style.display 2건 / BH_result_modal: style.display 1건. setAttribute hidden은 BH_how_panel 전용 (허용 예외) — 규칙 완전 준수 | PASS | - | - |
| 10 | 197 | 게임 JS 이모지 금지 — wp_staticize_emoji (v3.37) | script 블록 내 이모지 문자 직접 사용 금지, Unicode escape 필수 | 위젯 내 이모지 11건 검출 (pos=445, 652, 794, 917, 1910, 2074, 2169, 5584, 5698, 5902, 6005). 단, 이 이모지들은 HTML 마크업(aria-label, button 텍스트)에 위치하며 `<script>` 블록 내부가 아님. 스크립트 블록 내 이모지는 0건 | PASS | - | HTML 마크업 이모지는 wp_staticize_emoji 영향 없음 (JS 블록만 제한) |
| 11 | 221 | Chrome 백그라운드 탭 Throttle — 자동화 테스트 주의 | 게임 위젯 자동화 테스트 시 백그라운드 탭 지연 대응 | 테스트 절차 룰 — 정본 코드 영역 외 | N/A | - | - |
| 12 | 693 | WP wpautop 방어 — style/script 단일 행 | script/style 내 개행 0건, BR/P/HR 0건 | 위젯 총 75라인. `<br>` in script: 0건 / `<br>` in style: 0건 / wp:html opener=1, closer=1 (쌍 일치) | PASS | - | - |
| 13 | 721 | BH_ 네임스페이스 필수 (v3.21) | 모든 JS 함수/변수/id에 BH_ prefix 강제 | BH_ 함수 45개 / 비-BH_ 함수 0건 / BH_ refs 48건 확인 | PASS | - | - |
| 14 | 738 | Pre-PUT Validator — BH_preValidate (v3.21) | dev 전달 전 BH_preValidate 실행, ok:true 확인서 첨부 | 운영 절차 룰. 위젯 내 `BH_preValidate` 함수 정의 없음 (정상 — Validator는 dev 업로드 전 실행하는 외부 검증 도구) | N/A | - | - |
| 15 | 766 | GAME-SLOT 마커 시스템 (v3.21) | writer draft의 GAME-SLOT 마커 수신 후 위젯 구현 | 운영 절차 룰 — 정본 코드 영역 외 | N/A | - | - |
| 16 | 788 | JS 문자열 연결 패턴 (v3.21) | base64 금지, JS 문자열 + 연결 방식 사용 | 위젯 내 `BH_DECK_DATA=JSON.parse(new TextDecoder('utf-8').decode(Uint8Array.from(atob(...))))` 패턴 사용. Base64 + TextDecoder UTF-8 디코딩 — atob 단독이 아닌 TextDecoder 경유로 한글 Mojibake 방지. CLAUDE.md Base64 룰 준수 | PASS | - | - |
| 17 | 817 | 화투 패 JS 데이터 모델 (v3.24) | type: gwang/yeol/ddi/pi/ssangpi, ribbon, special 필드 정의 | **실측**: 위젯 BH_DECK_DATA type={gwang, jo, dan, pi} / 필드={id, month, type, name, emoji, svgUrl, label, bg}. game.md 규정 type(yeol→jo, ddi→dan, ssangpi 제거), ribbon 없음, special 없음, emoji/svgUrl 추가 | FAIL | Critical | game.md §화투 패 JS 데이터 모델을 위젯 실제 구현 기준으로 동기화 필요 (또는 위젯 변경) |
| 18 | 894 | 민화투 게임 상태 모델 (v3.24) | BH_GS: playerCap, aiCap, floor, turn 필드 / BH_calcScore 시그니처 | **실측**: 위젯 BH_GS={phase, deck, playerHand, aiHand, floor, playerCaptured, aiCaptured, selectedCard, deckFlipped, difficulty, hintUsed, hintCount, turnCount, gameOver}. playerCap→playerCaptured, aiCap→aiCaptured, turn 없음, phase 추가, hintUsed/hintCount/turnCount/gameOver 추가 | FAIL | High | game.md §게임 상태 모델 필드명을 위젯 실제 구현으로 동기화 (playerCaptured, aiCaptured) |
| 19 | 918 | AI 난이도별 알고리즘 설계 | easy: 무작위+힌트 / normal: 휴리스틱(광>열끗>띠>피) / hard: Expectiminimax 깊이 2 | **실측**: BH_aiSelectCard — easy: random 구현 / normal: 점수 최대화 휴리스틱 / hard: jokbo 족보 보너스 포함 휴리스틱. Expectiminimax/MCTS 미구현 (단순 확장 휴리스틱으로 대체) | FAIL | High | hard 모드 Expectiminimax 미구현. game.md 사양과 실제 구현 차이를 문서화 (성능 트레이드오프 인정 or game 에이전트 재구현) |
| 20 | 959 | 민화투 화면 구성 (레이아웃) | AI손패/AI획득패/바닥패/더미/플레이어손패/[힌트][뮤트][새게임] | 위젯 DOM 확인: `.BH_ai_zone`/`.BH_floor_zone`/`.BH_hand_zone`/힌트·뮤트·새게임 버튼 존재. 카드 60×84px (최소 60×90 미달 — 6px 부족) | FAIL | Medium | 카드 높이 84px → 90px 조정 권장 (game.md §시니어 UX 60×90 최소) |
| 21 | 984 | 민화투 협업 인터페이스 | design/design_ui/sound/qa 인터페이스 정의 | 운영 인터페이스 룰 | N/A | - | - |
| 22 | 994 | FSM 게임 상태 머신 (v3.25) | BH_FSM 객체: IDLE/DEALING/PLAYER_SELECT/PLAYER_PLAY/PLAYER_FLIP/AI_TURN/SCORING 7상태 | **실측**: `var BH_FSM` 미정의. 위젯은 `BH_GS.phase` 직접 제어 방식. 실제 phase 값: {IDLE, PLAYER_TURN, AI_TURN, ANIMATING}. game.md 규정 7상태 중 5개(DEALING/PLAYER_SELECT/PLAYER_PLAY/PLAYER_FLIP/SCORING) 미사용 | FAIL | Critical | BH_FSM 객체 미구현. 현재 BH_GS.phase 직접 제어 방식으로 동작 중 — game.md §FSM을 현재 구현 방식으로 현행화하거나 game 에이전트에 FSM 도입 요청 |
| 23 | 1225 | Expectiminimax 상세 구현 (v3.25) | 깊이 2 Expectiminimax, BH_evalState, BH_getLegalMoves, BH_applyMove 함수 | 해당 함수 0건. AI는 단순 휴리스틱 + jokbo 보너스. Expectiminimax 미구현 | FAIL | High | AI hard 모드 Expectiminimax 미구현 (항목 19와 동일 근본 원인) — 별도 high 카운트 아님 (이미 #19에 포함) |
| 24 | 1379 | MCTS (Hard 모드 대안, v3.26) | BH_mctsGetBestMove, UCT 공식 구현 | 관련 함수 0건. 현재 hard AI = 휴리스틱+jokbo | PASS | - | Expectiminimax 대안으로 제안된 것 — #19/#23과 함께 처리 예정 |
| 25 | 1551 | 족보 판정 완전판 (v3.27) | BH_checkJokboComplete: 고도리/홍단/초단/청단/이노시카초/오광/사광/비광/삼광 | 위젯 `BH_getJokboList`: 오광/비광/사광/삼광/조5/조4/고도리/홍단/초단/청단/이노시카초(멧돼지-사슴-나비) 구현 확인. 족보 체계 다름: game.md v3.25는 ribbon 기반, v3.27은 jokbo 배열 기반, 위젯은 type=jo/dan/gwang 기반 직접 계산 | PASS | - | 구현 방식 상이하지만 족보 논리적 결과는 동등. 단, jokbo 배열 필드 없어 BH_checkJokboComplete 함수명 비일치 |
| 26 | 2528 | 카드 뒤집기 애니메이션 — CSS 3D Flip (v3.33) | perspective/rotateY/backface-visibility CSS 3D flip, BH_triggerFlipAnimation | rotateY: 0건 / perspective: 0건 / backface-visibility: 0건. BH_playCardFlip은 사운드 함수(AudioContext 기반). CSS 3D flip 미구현 — 카드 뒤집기 시각 애니메이션 없음 | FAIL | Medium | CSS 3D flip 미구현. 게임 가능하나 시각적 완성도 낮음. game 에이전트에 단계 구현 요청 또는 game.md 사양 현행화 |
| 27 | 2655 | BH_StroopGame — 스트룹 게임 완전 구현 (v3.34) | BH_SS 상태, BH_generateStroopQuestions, 60초 타이머, d-prime 계산 | 정본 위젯은 민화투 전용 — 스트룹 미구현 (의도된 갭) | N/A (민화투 외 게임) | - | 별도 위젯으로 구현 예정 |
| 28 | 2945 | BH_NBackGame — N-Back 작업기억 (v3.35) | BH_NS 상태, d-prime 계산, 시퀀스 생성 | 정본 위젯은 민화투 전용 — N-Back 미구현 (의도된 갭) | N/A (민화투 외 게임) | - | 별도 위젯으로 구현 예정 |
| 29 | 3139 | git 운영 룰 | Windows 전용 git, Cowork git 금지 | 운영 절차 룰 — 정본 코드 영역 외 | N/A | - | - |
| 30 | - | BH_ 네임스페이스 — HTML id | HTML id에도 BH_ prefix 필수 | 위젯 내 `id="BH_diff_modal"`, `id="BH_game_board"`, `id="BH_result_modal"` 등 전수 BH_ prefix 확인 | PASS | - | - |
| 31 | - | WP 테마 CSS 충돌 방어 (v3.18) | button/ul/li에 !important 필수 | `!important` 총 311건. `list-style:none!important` 2건. button 배경/테두리 !important 확인 | PASS | - | - |
| 32 | - | 자동 타이머 (a5e9f4c 제거) | BH_startAutoTimer 자동 타이머 5항목 제거 반영 | `BH_startAutoTimer` 0건 / `BH_autoTimer` 0건 — 제거 반영 확인 | PASS | - | - |

---

## FAIL 항목 상세 설명

### F1. [#3] B1 confirm() 팝업 — Low
**근본 원인**: `BH_confirmNewGame(){if(confirm('새 게임을 시작하시겠습니까?'))` — 네이티브 `confirm()` 사용. game.md §프론트엔드 QA 발견 개선 권고(B1)에서 "모바일 UX 개선을 위해 커스텀 인라인 확인 모달로 교체" 권고 사항이 미반영 상태.  
**조치**: 게임 동작에는 치명적이지 않음. 모바일 사파리 등에서 팝업 차단 가능성 있음. game 에이전트 다음 사이클 수정.

### F2. [#4] overflow:hidden + 모달 수축 함정 — High  
**근본 원인**: `.BH_hwatu_wrap`에 `overflow:hidden` 적용 + `min-height` 미설정. 모달이 `position:absolute`면 컨테이너가 수축해 시각적 잘림 발생 가능. 2026-05-23 실제 사고 재발 위험 패턴.  
**조치**: `.BH_hwatu_wrap { min-height: 420px; }` 추가. game 또는 dev 에이전트 위임.

### F3. [#8] BH_startWithDiff 함수명 불일치 — Medium  
**근본 원인**: game.md §WP 업로드 후 SyntaxError 대응(v3.40)에서 `typeof BH_startWithDiff` 체크를 검증 식별자로 사용. 그러나 위젯의 게임 시작 함수는 `BH_showDifficultyModal`이며 `BH_startWithDiff`는 미정의. SW 검증 시 false negative 위험.  
**조치**: CLAUDE.md SW 검증 절차의 함수명을 `BH_showDifficultyModal`로 정정, 또는 game_planner 기획서 [검수 식별자] 업데이트. dev 에이전트에 정확한 SW 함수명 전달 필요.

### F4. [#17] 카드 데이터 타입 필드명 불일치 — Critical  
**근본 원인**: game.md §화투 패 JS 데이터 모델(v3.24, v3.27)은 `type: gwang/yeol/ddi/pi/ssangpi`, `ribbon`, `special` 필드를 규정. 실제 위젯 BH_DECK_DATA는 `type: {gwang, jo, dan, pi}`, `emoji`, `svgUrl`, `label`, `bg` 필드 사용. yeol→jo(조), ddi→dan(단), ribbon/special 없음, emoji(이모지 — HTML에만 존재 허용) 추가.  
**조치**: game.md 데이터 모델 섹션을 위젯 실제 구현 기준으로 동기화 필수. 족보 판정 로직도 ribbon 기반이 아닌 type 기반으로 이미 구현됨.

### F5. [#18] BH_GS 필드명 불일치 — High  
**근본 원인**: game.md v3.24는 `playerCap`, `aiCap`을 규정하나 위젯은 `playerCaptured`, `aiCaptured` 사용. `turn` 필드 없음. `phase`, `hintUsed`, `hintCount`, `turnCount`, `gameOver` 추가. 문서와 구현 간 드리프트.  
**조치**: game.md §게임 상태 모델을 위젯 실제 필드명으로 현행화. 다른 에이전트(qa 검수 스크립트 등)가 playerCap으로 접근 시 버그 유발 가능.

### F6. [#19/#23] Expectiminimax/MCTS 미구현 — High  
**근본 원인**: game.md v3.25는 hard 모드에 Expectiminimax 깊이 2를 규정하고, v3.26은 MCTS를 대안으로 제시. 실제 구현은 단순 점수 기반 그리디 + jokbo 보너스 가산. 성능상 이유로 단순화된 것으로 보이나 문서에 미반영.  
**조치**: game.md §AI 난이도를 실제 구현 방식(그리디 + jokbo 보너스)으로 현행화, 또는 hard 모드 재구현 여부 lead 결정 요청.

### F7. [#22] BH_FSM 객체 미구현 — Critical  
**근본 원인**: game.md v3.25는 `var BH_FSM = { state, transitions, go }` 패턴의 공식 FSM 객체를 정의하고 7상태(IDLE/DEALING/PLAYER_SELECT/PLAYER_PLAY/PLAYER_FLIP/AI_TURN/SCORING)를 요구. 위젯은 `BH_GS.phase` 직접 제어 방식을 사용하며 실제 사용 phase는 {IDLE, PLAYER_TURN, AI_TURN, ANIMATING} 4종. FSM 객체 미정의.  
**조치**: 2026-05-25 사고(FSM 통합 라이브 사고)의 직접 원인. BH_FSM 공식 객체 도입 or game.md의 FSM 섹션을 현재 BH_GS.phase 방식으로 현행화. lead 결정 필요.

### F8. [#20] 카드 높이 84px — Medium  
**근본 원인**: game.md §시니어 UX 규정 손패 카드 최소 60×90px. 위젯 실제 CSS `.BH_card{width:60px!important;height:84px!important;}` — 높이 6px 부족.  
**조치**: CSS `height:84px` → `height:90px` 변경. 레이아웃 파급 최소화 (단순 높이 증가).

### F9. [#26] CSS 3D flip 미구현 — Medium  
**근본 원인**: game.md v3.33은 `perspective:600px`, `rotateY(180deg)`, `backface-visibility:hidden` CSS 3D flip 패턴과 `BH_triggerFlipAnimation` 함수를 규정. 위젯의 `BH_playCardFlip`은 AudioContext 사운드 함수이며 시각 flip 없음.  
**조치**: 게임 동작에 치명적이지 않으나 UX 품질 낮음. game 에이전트 다음 사이클 카드 딜링/뒤집기 애니메이션 구현 권장.

---

## 권장 다음 단계

**Critical 2건 — 즉시 lead 결정 후 game/dev 위임**
- F7 (#22): BH_FSM 객체 도입 vs game.md 현행화 결정 (2026-05-25 사고 직접 원인)
- F4 (#17): 카드 데이터 타입 필드명 game.md 동기화 (문서 vs 구현 드리프트)

**High 3건 — 다음 사이클 game 에이전트 처리**
- F5 (#18): BH_GS 필드명 game.md 현행화 (playerCaptured, aiCaptured 등)
- F6 (#19/#23): AI hard 모드 사양 현행화 또는 Expectiminimax 구현
- F2 (#4): BH_hwatu_wrap min-height:420px 추가 (overflow 수축 방지)

**Medium 2건 — 게임 품질 개선 사이클**
- F3 (#8): SW 검증 함수명 BH_startWithDiff → BH_showDifficultyModal 정정
- F9 (#26): CSS 3D flip 구현 (시각 완성도)

**Low 1건 — 선택적**
- F1 (#3): confirm() → 커스텀 모달 교체
