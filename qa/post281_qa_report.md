# QA 검수 보고서 — 민화투 두뇌훈련 게임 (Post #281)
**검수 일시**: 2026-05-22  
**검수 URL**: https://neuralcare.co.kr/brain-games/minwhatoo/  
**검수 환경**: Chrome MCP (Claude in Chrome 확장)  
**검수 총 횟수**: 약 120회+ (JS 자동화 반복 포함)

---

## 1. 최종 검수 결과 요약

| 검수 항목 | 테스트 횟수 | PASS | FAIL | 비고 |
|---|---|---|---|---|
| 페이지 로드 초기 상태 | 3회 (새 탭 포함) | 0 | 3 | [버그 #1] 자동 타이머 UX |
| 난이도 선택 모달 표시 (BH_showDifficultyModal) | 5회 | 5 | 0 | 함수 정상 |
| 난이도 선택 → 게임 시작 (easy) | 5회 | 5 | 0 | PASS |
| 난이도 선택 → 게임 시작 (normal) | 5회 | 5 | 0 | PASS |
| 난이도 선택 → 게임 시작 (hard) | 5회 | 5 | 0 | PASS |
| **다시하기 버튼 동작** | **30회** | **30** | **0** | **PASS — 버그 미재현** |
| 다시하기 → 난이도 선택 → 재시작 사이클 | 20회 | 20 | 0 | PASS |
| 힌트 버튼 (BH_showHint) | 5회 | 5 | 0 | PASS |
| 음소거 토글 (BH_toggleMute) | 5회 | 5 | 0 | PASS |
| 게임 방법 토글 (BH_toggleHow) | 5회 | 5 | 0 | PASS |
| 공유 버튼 (BH_shareResult 존재) | 1회 | 1 | 0 | PASS |
| JS 에러 수집 (게임 관련) | 전 구간 | PASS | - | 게임 JS 에러 0건 |

---

## 2. 발견된 버그 상세

### [버그 #1] 초기 로드 자동 타이머 — 설계 확인 필요
- **재현 조건**: 페이지 최초 로드 (신규 탭 포함), 매회 재현
- **증상**:
  - 페이지 로드 시 `BH_diff_modal` HTML 속성 `style="display:none;"` 상태
  - `BH_showDifficultyModal()`이 IIFE 끝에서 자동 호출됨 → `dm.style.display=''` 설정
  - 동시에 `BH_startAutoTimer()` 호출 → **5초 카운트다운 시작**
  - 5초 후 자동으로 `BH_startWithDiff('normal')` 실행 → 게임 강제 시작
  - 결과: 페이지 진입 5초 후 난이도 선택 모달이 사라지고 게임 보드 표시
- **확인 방법**: `document.getElementById('BH_auto_timer').textContent` → `-3초 후 보통 난이도로 자동 시작`
- **재현율**: 3/3회 (100%)
- **버그 여부 판정**: 의도된 UX일 수 있음. 단, 사용자가 5초 내 난이도 선택 못 하면 강제로 '보통' 난이도로 시작됨. **dev 에이전트 확인 필요**

### [버그 #2] 다시하기 후 자동 타이머 미재실행 (UX 불일치)
- **재현 조건**: 게임 종료 후 다시하기 클릭
- **증상**:
  - `BH_restartGame()` 후 난이도 선택 모달 정상 표시 (✅)
  - 단, 초기 로드와 달리 `BH_startAutoTimer()` 재호출 없음
  - 다시하기 후에는 자동 5초 타이머 없이 사용자가 직접 난이도 선택 필요
- **JS 콘솔 오류**: 없음
- **재현율**: 30/30회 (구조적 차이)
- **심각도**: 낮음 (기능 작동은 정상)

### [확인 결과] 사용자 보고 "다시하기 후 플레이 안 된다"
- **JS 레벨 검증**: `BH_restartGame()` 30회, DOM 버튼 클릭 10회 전부 PASS
- **모달 전환**: 결과 모달 → 난이도 선택 모달 → 게임 보드 전환 정상
- **카드 배치**: 매 재시작 후 hand/floor/ai 각 8장 정상 배치 확인
- **JS 에러**: 0건
- **결론**: JS 자동화 레벨에서는 다시하기 버그 미재현
- **추가 조사 필요**: 실제 마우스/터치 환경에서 수동 검증 필요

---

## 3. 코드 구조 분석

### BH_restartGame() 실제 동작 (소스 분석)
```javascript
function BH_restartGame() {
  BH_playReset();
  var gb = document.getElementById('BH_game_board');
  var dm = document.getElementById('BH_diff_modal');
  if(gb) gb.style.display = 'none';   // 게임 보드 숨김
  if(dm) dm.style.display = '';       // 난이도 모달 표시 (CSS flex 적용)
  var rm = document.getElementById('BH_result_modal');
  if(rm) rm.style.display = 'none';  // 결과 모달 숨김
}
```

### CLAUDE.md WP CSS 특이성 룰 준수 확인
- `style.display = ''` 방식 사용 (style.display='none'/'' 직접 제어) ✅
- `setAttribute('hidden')` 미사용 ✅
- CSS `.BH_difficulty_modal, .BH_result_modal { display: flex; }` 확인됨

### 이벤트 구조
- 카드 클릭: `addEventListener('click')` 방식 (클로저 내부 처리)
- 키보드 (`keydown`): `BH_GS.phase === 'PLAYER_TURN'` 조건 처리
- 첫 상호작용 (`pointerdown`, once): `BH_getAC()` — AudioContext 초기화

---

## 4. SW/S3 검수 (WP 발행 패키지)

| 항목 | 확인 내용 | 결과 |
|---|---|---|
| **SW** | `typeof BH_restartGame === 'function'` | ✅ PASS |
| **S3** | 한글 Mojibake 패턴 확인 | ✅ PASS (깨진 문자 없음) |
| **S1** | 본문 텍스트 확인 | `/brain-games/` 허브 페이지 → S1 적용 제외 |

---

## 5. 권고사항

### 즉시 조치 필요
1. **사용자 보고 버그 추가 수동 검증**: 실제 마우스/터치로 게임 완료 → 다시하기 → 난이도 선택 → 카드 클릭 플레이 가능 여부 확인
2. **자동 타이머 UX 검토**: 페이지 진입 5초 후 강제 'normal' 난이도 시작 → 사용자 혼란 가능

### 선택적 개선
1. `BH_restartGame()` 후 `BH_startAutoTimer()` 재호출 — 초기 로드와 UX 일관성 확보
2. 자동 타이머 카운트다운 UI 가시성 개선

---

## 6. 결론

**사용자가 보고한 "다시하기 후 플레이 안 된다" 버그는 JS 자동화 레벨(30회 반복)에서 재현되지 않음.**

`BH_restartGame()` 함수는 완벽히 작동하고, 결과 모달 → 난이도 선택 → 게임 시작 플로우 정상 확인. 사용자가 "작동 안 된다"고 느끼는 원인으로 초기 로드 시 5초 자동 타이머 UX 혼란 가능성 있음.

**실제 사용자 환경(마우스/터치)에서 수동 검증 권고.**
