# Post #7 민화투 룰 분석 및 게임 수정 명세

**작성**: game_planner 에이전트 v1.8 / brain_health_1.0  
**날짜**: 2026-05-23  
**대상 파일**: `C:\Claude_code\widgets\post7_widget_v2.html`  
**목적**: 오너 버그 리포트 #3·#4·#5·#7·#8 처리를 위한 game 에이전트 구현 명세

---

## 민화투 룰 분석 요약 (표준 48장 2인전 기준)

### 패 구성 (총 48장)

| 구분 | 종류 | 장수 | 월 |
|---|---|---|---|
| 광 (gwang) | 학광·벚꽃광·달광·봉황광·우산광 | 5장 | 1·3·8·11·12월 |
| 열끗 (jo) | 조·공산새·난조·나비·멧돼지·기러기·술잔·사슴 | 8장 | 2·4·5·6·7·8·9·10월 |
| 띠 (dan) | 홍띠 3장 + 초띠 3장 + 청띠 4장 | 10장 | 1·2·3월(홍), 4·5·6월(초), 7·9·10·12월(청) |
| 쌍피 | 11월피1 + 12월피2 | 2장 | 11·12월 |
| 피 (pi) | 일반 피 | 23장 | 각 월 2장씩 |

**합계 검증**: 5 + 8 + 10 + 2 + 23 = 48장 ✅

### 2인전 초기 배분

| 구분 | 장수 | 비고 |
|---|---|---|
| 플레이어 손패 | **10장** | 오너 요청 #7 확인 |
| AI 손패 | **10장** | 오너 요청 #7 확인 |
| 바닥패 | **8장** | 앞면 공개 |
| 덱 (더미) | **20장** | 48 - 10 - 10 - 8 = 20 |

### 족보 조건 (민화투 표준)

| 족보명 | 조건 | 점수 |
|---|---|---|
| 오광 | 광 5장 전부 | +15점 |
| 사광 | 광 4장 (우산광 제외) | +4점 (일부 룰에서 상이) |
| 비광 | 광 3장 (우산광 포함) | +2점 |
| 삼광 | 광 3장 (우산광 제외) | +3점 |
| 고도리 | 2·4·8월 열끗 3장 | +5점 |
| 홍단 | **1·2·3월 띠** 3장 | +3점 |
| 초단 | **4·5·6월 띠** 3장 | +3점 |
| 청단 | **7·9·10월 띠** 3장 | +3점 |
| 피 보너스 | 10장 초과분 | 장당 +1점 |

> ⚠️ 단(띠) 족보는 **dan 타입** 카드로만 판별. jo(열끗)와 혼동 금지.

### 점수 계산 기준 (민화투 표준)

```
총점 = 광점수 + 피점수 + 족보점수
광: 장수에 따른 족보 점수 (오광15, 사광4, 비광2, 삼광3)
피: 쌍피 1장 = 피 2장으로 계산. 10장 기준 초과 시 +1점/장
족보: 고도리+5, 홍단/초단/청단 각 +3
```

---

## 현재 구현 vs 올바른 룰 비교표

| 항목 | 현재 구현 | 올바른 룰 | 수정 필요 |
|---|---|---|---|
| 플레이어 손패 | 8장 (슬라이스 0~7) | **10장** | ✅ #7 |
| AI 손패 | 8장 (슬라이스 8~15) | **10장** | ✅ #7 |
| 바닥패 | 8장 (슬라이스 16~23) | 8장 | - |
| 덱 | 24장 (슬라이스 24~) | **20장** | ✅ #7 자동해결 |
| 패수 표시 | 광/조/피 3종 | **광/열끗/띠/피** 4종 | ✅ #8 |
| 쌍피 카운트 | value 무시, 1장=1점 | **쌍피 1장=피 2장** | ✅ #8 |
| 홍단 조건 | `gb=[1,2,3] + jo 배열` | `[1,2,3]월 dan 배열` | ✅ #5 |
| 초단 조건 | `gd=[4,5,7] + jo 배열` | `[4,5,6]월 dan 배열` | ✅ #5 |
| 청단 조건 | `gc=[6,9,10] + jo 배열` | `[7,9,10]월 dan 배열` | ✅ #5 |
| 획득 패 정렬 | 획득 순서 그대로 출력 | **광/열끗/띠/피** 순 정렬 | ✅ #3 |
| 상대 획득 패 | 표시 안 됨 | **AI 획득 패 영역 추가** | ✅ #4 |
| deck 타입 오류 | m12_dan=yul, m12_pi1=dan | m12_dan=jo, m12_pi1=pi | ✅ #5 |

---

## game 에이전트 수정 명세

### #7 — 초기 패 배분 수정

**파일 위치**: `BH_initGame` 함수

**현재 코드**:
```js
BH_GS.playerHand = shuffled.slice(0, 8);
BH_GS.aiHand = shuffled.slice(8, 16);
BH_GS.floor = shuffled.slice(16, 24);
BH_GS.deck = shuffled.slice(24);
```

**수정 후**:
```js
BH_GS.playerHand = shuffled.slice(0, 10);   // 10장
BH_GS.aiHand = shuffled.slice(10, 20);       // 10장
BH_GS.floor = shuffled.slice(20, 28);        // 8장
BH_GS.deck = shuffled.slice(28);             // 20장 (48-10-10-8=20)
```

**검증**: 합계 10+10+8+20 = 48장 ✅

**UI 연동**: 게임 방법 텍스트 "손패(8장)" → "손패(10장)"으로 변경 필요.

---

### #8 — 패수 카운트 표시 수정

**파일 위치**: `BH_renderCaptured`, `BH_renderAIHand` 함수

**현재 카운트 로직**:
```js
var gc = captured.filter(c => c.type === 'gwang').length;
var jc = captured.filter(c => c.type === 'jo').length;
var pc = captured.filter(c => c.type === 'pi').length;
cnt.textContent = '광'+gc+' 조'+jc+' 피'+pc;
```

**수정 후 카운트 로직**:
```js
var gwangCnt  = captured.filter(c => c.type === 'gwang').length;
var joCnt     = captured.filter(c => c.type === 'jo').length;
var danCnt    = captured.filter(c => c.type === 'dan').length;
// 쌍피: value=2인 pi는 피 2장으로 계산
var piCnt     = captured.filter(c => c.type === 'pi')
                        .reduce((acc, c) => acc + (c.value || 1), 0);
cnt.textContent = '광'+gwangCnt+' 열'+joCnt+' 띠'+danCnt+' 피'+piCnt;
```

**쌍피 카드 목록** (deck에서 value=2인 pi):
- `m11_pi1` (11월 피1, value=2) — 쌍피
- `m12_pi2` (12월 쌍피, value=2) — 쌍피

---

### #3 — 획득 패 정렬 수정

**파일 위치**: `BH_renderCaptured` 함수

**정렬 우선순위**: 광(gwang) > 열끗(jo) > 띠(dan) > 피(pi)

**수정 후 정렬 코드**:
```js
function BH_sortCaptured(arr) {
    var order = { gwang: 0, jo: 1, dan: 2, pi: 3 };
    return arr.slice().sort(function(a, b) {
        var ao = order[a.type] !== undefined ? order[a.type] : 4;
        var bo = order[b.type] !== undefined ? order[b.type] : 4;
        if (ao !== bo) return ao - bo;
        return a.month - b.month;  // 같은 타입 내에서 월 순
    });
}
```

**적용 위치**:
```js
// BH_renderCaptured 내
var sorted = BH_sortCaptured(BH_GS.playerCaptured);
sorted.forEach(function(card) { ... });
```

---

### #4 — AI 획득 패 표시 영역 추가

**현재 HTML 구조**: AI 손패(뒷면) 표시 영역만 있음 (`BH_ai_zone`)

**추가 필요**: AI 획득 패 전용 영역

**HTML 추가** (`BH_ai_zone` 아래에 삽입):
```html
<div class="BH_ai_captured_zone" id="BH_ai_captured_zone" aria-label="AI 획득 카드"></div>
```

**CSS 추가**:
```css
.BH_ai_captured_zone {
  display: flex !important;
  flex-wrap: wrap !important;
  gap: 3px !important;
  min-height: 30px !important;
  background: rgba(200,50,50,0.07) !important;
  border-radius: 8px !important;
  padding: 4px !important;
  margin-bottom: 6px !important;
}
```

**JS 렌더링 함수 추가**:
```js
function BH_renderAICaptured() {
    var z = document.getElementById('BH_ai_captured_zone');
    if (!z) return;
    z.innerHTML = '';
    var sorted = BH_sortCaptured(BH_GS.aiCaptured);
    sorted.forEach(function(card) {
        var el = BH_makeCardEl(card, { small: true });
        z.appendChild(el);
    });
}
```

**`BH_renderBoard` 내에 호출 추가**:
```js
BH_renderAICaptured();
```

---

### #5 — deck 데이터 타입 오류 수정 (DECK_DATA)

**분석 결과**: Base64 인코딩된 BH_DECK_DATA 내 2개 카드 타입 오류 확인.

| 카드 ID | 현재 type | 올바른 type | 근거 |
|---|---|---|---|
| `m12_dan` | `yul` | `jo` | 12월 번개는 열끗(jo)로 처리 |
| `m12_pi1` | `dan` | `pi` | 12월에 청띠 없음. 이 카드는 피임 |

> ⚠️ 주의: `m12_dan`의 이름은 "12월 열끗"으로 이미 올바름. type만 yul→jo로 변경.  
> ⚠️ `m12_pi1`의 이름은 "12월 단"으로 되어 있으나 실제 민화투에서 12월 청띠는 별도 카드.  
>    12월 구성: 우산광(gwang) + 번개(jo) + 청띠(dan) + 쌍피(pi, value=2) 이므로  
>    `m12_pi1`은 "12월 청띠"로 type=dan이 맞을 수 있음.  
>    **확인 필요**: 12월 카드 4장 구성 재검토 후 결정.

**안전한 수정 방향** (민화투 12월 구성 확정 후 적용):
- 12월: 우산광(gwang) + 번개(jo) + 청띠(dan) + 쌍피(pi, value=2)
- `m12_dan` → type=`jo`, name="12월 번개" 로 수정
- `m12_pi1` → type=`dan`, name="12월 청띠" 유지 (현재도 dan이라 맞음)
- `m12_dan`의 type만 `yul` → `jo` 변경

**deck 데이터 수정 방법**: Python으로 JSON 디코딩 → type 수정 → base64 재인코딩.

---

### #5 — 족보 조건 오류 수정 (BH_getJokboList / BH_calcScoreFromCaptured)

**현재 잘못된 조건들**:

```js
// 현재 오류 코드 (jo 배열로 dan(띠) 검색)
var gb=[1,2,3]; if(gb.every(m=>jo.some(c=>c.month===m))) list.push('청단(3점)');  // 틀림
var gc=[6,9,10]; if(gc.every(m=>jo.some(c=>c.month===m))) list.push('홍단(3점)'); // 틀림
var gd=[4,5,7]; if(gd.every(m=>jo.some(c=>c.month===m))) list.push('초단(3점)');  // 틀림
```

**수정 후 올바른 조건들**:

```js
// dan(띠) 배열로 변경
var dan = captured.filter(c => c.type === 'dan');

// 홍단: 1·2·3월 띠
var hongdan = [1,2,3];
if (hongdan.every(m => dan.some(c => c.month === m))) list.push('홍단(3점)');

// 초단: 4·5·6월 띠 (기존 코드의 7월은 오류 - 6월로 수정)
var chodan = [4,5,6];
if (chodan.every(m => dan.some(c => c.month === m))) list.push('초단(3점)');

// 청단: 7·9·10월 띠 (기존 코드 완전히 교체)
var cheongdan = [7,9,10];
if (cheongdan.every(m => dan.some(c => c.month === m))) list.push('청단(3점)');
```

**동일 수정을 `BH_calcScoreFromCaptured`에도 적용** (점수 계산 함수도 같은 오류).

---

### 추가 수정 — UI 표시 텍스트

**게임 방법 텍스트** (`BH_how_panel` 내):
```
현재: "1. 손패(8장)에서 카드를 선택하세요."
수정: "1. 손패(10장)에서 카드를 선택하세요."
```

**점수판 레이블** (`BH_score_panel` 내):
- `BH_my_counts`, `BH_ai_counts` 표시 형식: `광0 열0 띠0 피0` (4종)

---

## 수정 우선순위 및 의존성

```
우선순위 1 (독립 수정):
  ① #7 BH_initGame 슬라이스 인덱스 변경 (8→10장)
  ② #5 deck JSON 타입 오류 수정 (m12_dan: yul→jo) + base64 재인코딩
  ③ #5 BH_getJokboList / BH_calcScoreFromCaptured 족보 조건 수정

우선순위 2 (①②③ 완료 후):
  ④ #8 패수 카운트 로직 수정 (4종 분류 + 쌍피 value 반영)
  ⑤ #3 BH_sortCaptured 정렬 함수 추가 + BH_renderCaptured 적용
  ⑥ #4 AI 획득 패 영역 HTML/CSS/JS 추가
```

---

## 검수 식별자

- **SW 함수명**: `BH_startWithDiff` (기존 유지)
- **S1**: 포스트 본문 500자 이상 (위젯과 별개)
- **S3**: 한글 Mojibake 0건

---

## 메모 — 12월 카드 구성 최종 확인 요청

현재 deck 데이터에서 12월 카드:
- `m12_dan` (type=yul, name="12월 열끗") — 번개 카드, yul 타입은 존재하지 않아야 함
- `m12_jo` (type=gwang, name="12월 광") — 우산광
- `m12_pi1` (type=dan, name="12월 단") — 청띠
- `m12_pi2` (type=pi, name="12월 쌍피", value=2) — 쌍피

**결론**: 12월 구성은 광(gwang)+번개(jo)+청띠(dan)+쌍피(pi,value=2) 4장으로 올바름.  
단, `m12_dan`의 type이 `yul`(존재하지 않는 타입)로 잘못 설정됨 → `jo`로 수정 필수.

게임 내 점수 계산에서 `yul` 타입은 어느 카테고리에도 매칭되지 않아  
12월 번개 카드가 **열끗 카운트에서 완전히 누락**되고 있음.

---

*game_planner 에이전트 v1.8 작성 완료 — 2026-05-23*
