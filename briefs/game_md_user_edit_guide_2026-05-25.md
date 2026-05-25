# game.md 사용자 직접 편집 가이드 — 2026-05-25 (v3.46 마무리)

**대상 파일**: `C:\Claude_code\.claude\agents\game.md`
**배경**: ❓-C 작업 중 보안 분류기가 dev의 .md 대규모 편집을 차단(Self-Modification). 사용자 옵션 ㉠ "직접 편집" 선택.
**작업 분량**: F5~F9 5건 (dev 초안) + F4 잔존 정리 3건 + 오타 1건 = **총 9건**

---

## 📋 적용 방법

게임 코드 에디터(VSCode 권장)로 `game.md`를 열고, 아래 각 항목의 **라인 번호**로 이동 → 기존 내용을 **교체** 또는 **삽입**.

라인 번호는 현재 v3.46 상태 기준. 위에서 아래로 순서대로 적용하면 라인 번호 밀림 없음 (긴 블록 교체 시 이하 라인 자동 이동).

---

## ① 라인 821 — F4 오타 정정 (★ 1줄)

**기존**:
```
> ★ v3.45 → v3.46 현행화 (2026-05-25): 정본 코드 동기화 — yeol→jo, ddi→dan, ribbon/special 폐기, emoji/svgUrl/label/bg 추가
```

**교체**:
```
> ★ v3.45 → v3.46 현행화 (2026-05-25): 정본 코드 동기화 — yeol→jo, ddi→dan, ribbon/special 폐기, emoji/svgUrl/label/bg 추가
```

(`v3.46 → v3.46` → `v3.45 → v3.46`)

---

## ② 라인 849~867 — F5 [#18] BH_GS 필드명 + F4 잔존 일부

**기존** (라인 849~867):
```javascript
// ★ 게임 전체 상태 — 단일 객체로 관리
var BH_GS = {
  deck:        [],   // 남은 더미 (배열 앞이 맨 위)
  floor:       [],   // 바닥패 (월별 그룹: {month, cards[]})
  playerHand:  [],   // 플레이어 손패
  aiHand:      [],   // AI 손패 (플레이어에게 비공개)
  playerCap:   [],   // 플레이어 획득 패
  aiCap:       [],   // AI 획득 패
  turn:        'player',    // 'player' | 'ai'
  phase:       'select',    // 'select'(손패 선택) | 'flip'(더미 뒤집기) | 'result'
  difficulty:  'normal',    // 'easy' | 'normal' | 'hard'
  selectedCard: null,       // 현재 선택된 손패 카드 id
};

// ★ 점수 계산 함수 시그니처 (구현 시 참고)
// BH_calcScore(capturedCards) → { gwang, yeol, ddi, jokbo, total }
// BH_checkJokbo(capturedCards) → { hongdan, chodan, cheongdan, godori }
```

**교체**:
```javascript
// ★ 게임 전체 상태 — 단일 객체로 관리 (v3.46 현행화 — 정본 post7_widget.html 실측 기준)
// ★ v3.45 → v3.46 현행화 (2026-05-25): playerCap→playerCaptured, aiCap→aiCaptured, turn 제거, phase 4상태로 현행화, hintUsed/hintCount/turnCount/gameOver 추가
var BH_GS = {
  phase:         'IDLE',     // 'IDLE' | 'PLAYER_TURN' | 'AI_TURN' | 'ANIMATING'
  deck:          [],         // 남은 더미
  playerHand:    [],         // 플레이어 손패
  aiHand:        [],         // AI 손패
  floor:         [],         // 바닥패
  playerCaptured:[],         // 플레이어 획득 패 (구버전 playerCap 폐기)
  aiCaptured:    [],         // AI 획득 패 (구버전 aiCap 폐기)
  selectedCard:  null,
  deckFlipped:   null,
  difficulty:    'normal',
  hintUsed:      false,
  hintCount:     0,
  turnCount:     0,
  gameOver:      false,
};

// ★ 점수 계산 함수 시그니처 (v3.46 현행화 — 정본 BH_calcScore 실측 기준)
// BH_calcScore(capturedCards) → { gwang, jo, dan, jokbo, total }   (구버전 yeol→jo, ddi→dan)
// BH_checkJokbo(capturedCards) → { hongdan, chodan, cheongdan, godori }
```

---

## ③ 라인 887 — F4 잔존 priority 배열 정정 (★ 1줄)

**기존**:
```javascript
  var priority = ['gwang','yeol','ddi','pi','ssangpi'];
```

**교체**:
```javascript
  var priority = ['gwang','jo','dan','pi'];  // v3.46 현행화: yeol→jo, ddi→dan, ssangpi 폐기
```

---

## ④ 라인 897~ — F6 [#19] AI Hard 섹션 + Expectiminimax 보류 박스

### ④-1. 라인 897 부근 §AI 난이도별 알고리즘 설계 §어려움(Hard) 섹션

**기존** (라인 897부터 시작하는 `### 어려움 (Hard) — Expectiminimax (깊이 2)` 블록 전체 — 다음 헤딩 전까지)

**교체**:
```
### 어려움 (Hard) — 휴리스틱 + 족보(jokbo) 보너스 가산

> ★ v3.46 현행화 (2026-05-25): Expectiminimax 미구현. 정본은 그리디 휴리스틱 + jokbo 보너스 방식.

정본 `BH_aiSelectCard` 실측 알고리즘:
1. 손패 중 바닥과 짝 맞는 카드 우선 선택
2. 짝 카드 중 jokbo(고도리/홍단/초단/청단/이노시카초 등) 완성/근접 카드에 보너스 가산
3. 동점 시 type 우선순위: gwang > jo > dan > pi
4. 짝 없으면 가장 낮은 가치 카드 버림 (피 우선)

성능 트레이드오프: 깊이 탐색 미실행 → 응답 빠름·예측 단순. 향후 강화 사이클에서 Expectiminimax/MCTS 재검토.
```

### ④-2. 라인 1178 (§Expectiminimax 섹션 상단) — 보류 박스 추가

**기존** (라인 1178):
```
## 🎯 Expectiminimax 상세 구현 ★ v3.25 신설
```

**교체** (위 줄 바로 다음에 박스 1줄 추가):
```
## 🎯 Expectiminimax 상세 구현 ★ v3.25 신설

> ⚠️ 보류 — 향후 성능 개선 사이클에서 재검토. 현재 정본은 휴리스틱+jokbo 보너스 방식으로 구현됨. 아래 사양은 참조용으로 보존. ★ v3.46 (2026-05-25)
```

### ④-3. 라인 1332 (§MCTS 섹션 상단) — 보류 박스 추가

**기존** (라인 1332):
```
## 🤖 MCTS (Monte Carlo Tree Search) — Hard 모드 대안 ★ v3.26 신설
```

**교체** (위 줄 바로 다음에 박스 1줄 추가):
```
## 🤖 MCTS (Monte Carlo Tree Search) — Hard 모드 대안 ★ v3.26 신설

> ⚠️ 보류 — 정본 미구현. Expectiminimax 대안으로 v3.26에 제안됨. 향후 강화 사이클 대상. ★ v3.46 (2026-05-25)
```

---

## ⑤ 라인 947 — F7 [#22] FSM 섹션 상단 박스 추가

**기존** (라인 947):
```
## 🔄 FSM 게임 상태 머신 (Finite State Machine) ★ v3.25 신설
```

**교체** (위 줄 바로 다음에 박스 추가):
```
## 🔄 FSM 게임 상태 머신 (Finite State Machine) ★ v3.25 신설

> ★ 2026-05-25 FSM 통합 라이브 사고 후 정본은 BH_GS.phase 직접 제어 방식으로 안정화. 실제 사용 phase: {IDLE, PLAYER_TURN, AI_TURN, ANIMATING} 4종. 아래 7상태 BH_FSM 객체는 미구현 — 향후 신중 재검토 영역. ★ v3.46 (2026-05-25)
```

---

## ⑥ 라인 1042~1086 — F4 잔존 §족보 판정 영역 보류 박스 (★ 큰 영역)

이 영역(라인 1042~1086)은 ribbon 기반 족보 판정 로직이지만, 정본 위젯은 type+month 직접 계산 방식 사용. 코드 보존 + 보류 박스 추가.

**라인 1042 바로 위에 박스 1개 삽입** (즉 `hongdan:` 행 위):

```
> ⚠️ 참조용 보존 — 아래 ribbon 기반 족보 판정은 v3.27 사양. 정본 위젯은 type+month 직접 계산 방식으로 다르게 구현. 신규 게임 구현 시 정본 BH_getJokboList 패턴 참조 권장. ★ v3.46 (2026-05-25)
```

---

## ⑦ 라인 1238 — F8 [#20] 카드 크기 행 교체

**기존** (라인 1238):
```
| 카드 크기(손패) | 60×90px | 80×120px | 손가락 터치 편의 |
```

**교체**:
```
| 카드 크기(손패) | 60×84px 이상 (시니어 UX 검수 허용), 60×90px 권장 | 80×120px | ★ v3.46 현행화: 정본 60×84px 실측 기준 완화 |
```

> ⚠️ 라인 931에도 `손패 카드: 60×90px (최소) / 80×120px (권장)` 별도 표기가 있음. 이 줄도 함께 정정 권장:
> 기존: `- 손패 카드: 60×90px (최소) / 80×120px (권장)`
> 교체: `- 손패 카드: 60×84px 이상 / 80×120px (권장) — ★ v3.46 현행화 (정본 84px 실측 기준)`

---

## ⑧ 라인 1432~ — F4 잔존 §별도 카드 정의 영역 보류 박스

이 영역(라인 1432~약 1520)은 yeol/ti/pi1/pi2 표기의 별도 카드 데이터 정의 (v3.25 시점 사양). 정본과 다른 표기 체계. 코드 보존 + 보류 박스 추가.

**라인 1428 부근 (`족보 계산은 ID가 아닌...` 줄 위)에 박스 1개 삽입**:

```
> ⚠️ 참조용 보존 — 아래 카드 정의는 v3.25 사양(yeol/ti/pi1/pi2 표기). 정본 v3.46은 §화투 패 JS 데이터 모델(라인 819) 참조 (jo/dan 표기). 신규 게임 구현 시 정본 사양 우선. ★ v3.46 (2026-05-25)
```

---

## ⑨ 라인 2481 — F9 [#26] CSS 3D flip 섹션 상단 박스 추가

**기존** (라인 2481):
```
## 🎮 카드 뒤집기 애니메이션 — CSS 3D Flip v3.33 신설
```

**교체** (위 줄 바로 다음에 박스 추가):
```
## 🎮 카드 뒤집기 애니메이션 — CSS 3D Flip v3.33 신설

> ⚠️ 보류 — 정본 미구현. 현재 `BH_playCardFlip`은 사운드 함수(AudioContext 기반). CSS 3D flip 시각 애니메이션은 향후 시각 품질 개선 사이클 대상. 아래 사양 참조용 보존. ★ v3.46 (2026-05-25)
```

---

## ✅ 완료 검증 체크리스트

편집 완료 후 lead에게 보고 시 아래 체크:

- [ ] ① 라인 821 오타 정정 (v3.46→v3.46 → v3.45→v3.46)
- [ ] ② 라인 849~867 BH_GS 코드블록 교체 (4상태 phase + playerCaptured/aiCaptured 등)
- [ ] ③ 라인 887 priority 배열 정정
- [ ] ④-1 §AI Hard 섹션 교체 (휴리스틱+jokbo 보너스 형태)
- [ ] ④-2 §Expectiminimax 보류 박스 추가
- [ ] ④-3 §MCTS 보류 박스 추가
- [ ] ⑤ §FSM 사고 박스 추가
- [ ] ⑥ §족보 판정 보류 박스 추가
- [ ] ⑦ 라인 1238 + 931 카드 크기 완화
- [ ] ⑧ §별도 카드 정의 보류 박스 추가
- [ ] ⑨ §CSS 3D flip 보류 박스 추가

편집 완료 후 lead에게 "game.md 9건 직접 편집 완료" 보고 → lead가 qa 사후 검증 위임.

---

## 🔄 편집 후 후속 처리 (lead 책임)

1. qa 사후 검증 — 9건 적용 정합성 + game.md 자체 무결성 확인
2. 스냅샷 — `C:\Claude_code\2026-05-25-agent\game.md` 복사
3. agent_changelog.xlsx `game` 탭 행 추가
4. git commit + push 결정 (F2 위젯 수정 + game.md 변경 + 사용자 안내 가이드)
5. 핸드오프 갱신
