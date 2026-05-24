# QA 보고서 — Post #7 민화투 300판 재검수

**검수일**: 2026-05-21  
**검수 방식**: Python 게임 로직 시뮬레이션 300판 + Chrome MCP 브라우저 검증  
**판정**: ✅ **전 항목 PASS**

---

## 1. S1·S3·SW 기본 검증

| 항목 | 결과 | 비고 |
|---|---|---|
| S1 본문 500자 이상 | ✅ PASS | 3744자 확인 |
| S3 Mojibake 0건 | ✅ PASS | Latin-1 깨짐 패턴 0건 |
| SW BH_startWithDiff 함수 로드 | ✅ PASS | typeof === 'function' |
| SW BH_restartGame 함수 로드 | ✅ PASS | typeof === 'function' (Bug #1 수정 반영) |

---

## 2. 300판 자동 시뮬레이션 결과

**방법**: 위젯 소스에서 순수 게임 로직 추출 → Python으로 300판 실행  
**난이도**: easy / normal / hard 순환 (각 100판)

| 항목 | 결과 |
|---|---|
| 총 게임 수 | 300판 |
| 에러(크래시) | **0건** ✅ |
| 카드 총합 오류 | **0건** ✅ (48장 항상 유지) |
| 승리 / 패배 / 무승부 | 162 / 130 / 8 |
| 족보 발생 게임 수 | 297 / 300 (99%) |
| 최소 턴 / 최대 턴 | 8 / 8 (정상 — 손패 8장) |

### 족보 발생 현황 (전체)

| 족보 | 발생 횟수 |
|---|---|
| 오광 | 141 |
| 조4 | 233 |
| 조5 | 163 |
| 사광 | 54 |
| 삼광 | 56 |
| 비광 | 26 |
| 피1점 | 52 |
| 피2점 | 37 |
| 피3점 | 13 |
| 피4점 | 11 |
| 피5점 | 5 |
| 피6점 | 1 |
| 초단 | 27 |
| 홍단 | 17 |
| 청단 | 12 |
| 고도리 | 10 |

→ **7종 족보 모두 발생 확인** ✅

---

## 3. Bug #1 수정 검증 (BH_restartGame 전역 노출)

| 검증 항목 | 결과 |
|---|---|
| `typeof window.BH_restartGame === 'function'` | ✅ true |
| BH_restartGame() 호출 후 dm.style.display | ✅ '' (diff 모달 복원) |
| BH_restartGame() 호출 후 gb.style.display | ✅ '' (게임 보드 유지) |

---

## 4. Bug #2 수정 검증 (재시작 후 난이도 모달 클리핑 해소)

**재현 조건**: BH_restartGame() → BH_startWithDiff('normal')

| 검증 항목 | 결과 |
|---|---|
| dm.style.display | ✅ 'none' (diff 모달 숨김) |
| gb.style.display | ✅ '' (게임 보드 표시) |
| dm_h (height) | ✅ 0px (완전 숨김) |
| gb_h (height) | ✅ 693px (클리핑 없음, 정상) |
| hand 카드 수 | ✅ 8장 |
| floor 카드 수 | ✅ 8장 |
| deck | ✅ 24장 |
| turn | ✅ "내 차례" |

---

## 5. 종합 판정

| 카테고리 | 결과 |
|---|---|
| 게임 로직 안정성 (300판) | ✅ PASS — 크래시 0건, 카드 총합 오류 0건 |
| 족보 판정 | ✅ PASS — 7종 전종 발생 확인 |
| Bug #1 (BH_restartGame 전역 노출) | ✅ PASS |
| Bug #2 (재시작 후 클리핑 해소) | ✅ PASS |
| S1·S3·SW 기본 | ✅ PASS |

**최종 판정: ✅ 300판 검수 PASS — Post #7 민화투 품질 확인 완료**
