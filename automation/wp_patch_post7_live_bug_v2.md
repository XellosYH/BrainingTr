# WP Page #303 라이브 타겟 PATCH 스니펫 v2
**작성**: dev 에이전트 v6.55 / 2026-05-25
**대상**: https://neuralcare.co.kr/brain-games/minwhatoo/ (WP Page ID: 303)
**목적**: v1 SyntaxError 회피 — 한글 0건 + 작은따옴표 0건 재설계

---

## v1 SyntaxError 원인 분석

| 원인 | 내용 |
|---|---|
| OLD_A 한글 24자 | `초 후 보통 난이도로 자동 시작` — 마크다운 복사 시 편집기가 `'` (U+0027) 를 `'`(U+2018) 로 자동 변환 가능 |
| OLD_A 작은따옴표 6개 | JS 문자열 내 `'BH_auto_timer'`, `'초 후...'` 등 |
| OLD_B 작은따옴표 있음 | `'BH_overlay_card'` 등 |
| 결과 | 콘솔 붙여넣기 시 curly quote 혼입 → `Uncaught SyntaxError: Invalid or unexpected token` |

**v2 해결 원칙**: OLD_A는 `"var sec=5;"` (한글 0건·따옴표 0건) 로만 교체. OLD_B는 `"||" + "(isAI?480:800);card.classList.add"` 를 anchor 삼아 정규식 교체.

---

## 사전 검증 결과 (2026-05-25)

| 항목 | 정본 post7_widget.html | 결론 |
|---|---|---|
| `var sec=5;` | 0건 | 정본 Bug A 수정 완료 |
| `var sec=15;` | 1건 | 정본 정상 |
| `BH_hideOverlay();if(typeof onComplete` | 3건 | 정본 Bug B 수정 완료 |
| `\|\|(isAI?480:800);card.classList.add` | **1건** | Bug B anchor 패턴 unique |
| 파일 크기 | 83,741 chars | |

라이브 WP에는 구 버전(sec=5, hideOverlay 없음)이 남아있으므로 아래 스니펫으로 동기화.

---

## 메인 스니펫 v2 (한글 0건 · 따옴표 0건 보장)

> 전제: WP 관리자 로그인 상태. neuralcare.co.kr 탭 열린 상태.
> 따옴표는 **전부 큰따옴표** `"` — 작은따옴표·한글 문자 없음.

```javascript
(async () => {
  const nonce = (await (await fetch("/wp-admin/admin-ajax.php?action=rest-nonce", {
    credentials: "include"
  })).text()).trim();
  if (!nonce || nonce === "false" || nonce === "0") {
    console.error("[1] Nonce fail");
    return;
  }
  console.log("[1] OK nonce:", nonce.slice(0, 8));

  const pageResp = await fetch("/wp-json/wp/v2/pages/303?context=edit", {
    headers: {"X-WP-Nonce": nonce},
    credentials: "include",
    cache: "no-store"
  });
  if (!pageResp.ok) { console.error("[2] GET fail", pageResp.status); return; }
  let raw = (await pageResp.json()).content.raw;
  console.log("[2] OK raw len:", raw.length);

  // Bug A: var sec=5 -> var sec=15 (no Korean, no single quotes)
  const cntA = (raw.match(/var sec=5;/g) || []).length;
  if (cntA === 0) {
    console.warn("[3a] SKIP A (already patched or pattern not found)");
  } else if (cntA > 1) {
    console.error("[3a] FAIL A duplicates:", cntA);
    return;
  } else {
    raw = raw.replace("var sec=5;", "var sec=15;");
    console.log("[3a] OK A patched");
  }

  // Bug B: BH_animateCardReveal + unique anchor -> insert BH_hideOverlay()
  // Anchor: ||(isAI?480:800);card.classList.add  (1 match in whole file)
  // Target pattern after anchor: ...setTimeout(function(){if(typeof onComplete
  // Replace with:               ...setTimeout(function(){BH_hideOverlay();if(typeof onComplete
  const ANCHOR = "||(isAI?480:800);card.classList.add";
  const anchorIdx = raw.indexOf(ANCHOR);
  if (anchorIdx === -1) {
    console.warn("[3b] SKIP B (anchor not found)");
  } else {
    const searchFrom = anchorIdx;
    const searchEnd = searchFrom + 500;
    const segment = raw.slice(searchFrom, searchEnd);
    const OLD_INNER = "setTimeout(function(){if(typeof onComplete";
    const NEW_INNER = "setTimeout(function(){BH_hideOverlay();if(typeof onComplete";
    if (!segment.includes(OLD_INNER)) {
      console.warn("[3b] SKIP B (OLD pattern not found in window — already patched)");
    } else {
      const before = raw.slice(0, searchFrom);
      const after = raw.slice(searchFrom);
      raw = before + after.replace(OLD_INNER, NEW_INNER);
      console.log("[3b] OK B patched");
    }
  }

  const patchResp = await fetch("/wp-json/wp/v2/pages/303", {
    method: "POST",
    headers: {"X-WP-Nonce": nonce, "Content-Type": "application/json"},
    credentials: "include",
    body: JSON.stringify({content: raw})
  });
  if (!patchResp.ok) {
    console.error("[4] PATCH fail", patchResp.status, await patchResp.text().then(t => t.slice(0, 200)));
    return;
  }
  console.log("[4] OK PATCH id:", (await patchResp.json()).id);

  const vraw = (await (await fetch("/wp-json/wp/v2/pages/303?context=edit", {
    headers: {"X-WP-Nonce": nonce}, credentials: "include", cache: "no-store"
  })).json()).content.raw;

  const r1 = vraw.includes("var sec=15;");
  const r2 = !vraw.includes("var sec=5;");
  const r3 = vraw.includes("BH_hideOverlay();if(typeof onComplete");
  console.log("[5] sec=15:", r1 ? "PASS" : "FAIL");
  console.log("[5] sec=5 gone:", r2 ? "PASS" : "FAIL");
  console.log("[5] hideOverlay added:", r3 ? "PASS" : "FAIL");
  console.log("[5] raw len:", vraw.length);
  console.log("[5] ALL:", (r1 && r2 && r3) ? "PASS" : "FAIL");
})();
```

**한글 0건 · 작은따옴표 0건 확인**: 위 코드블록 내 한글 문자 없음. 모든 문자열 리터럴 `"큰따옴표"` 사용.

---

## Fallback — 분할 실행 5단계

메인 스니펫도 SyntaxError 발생 시(환경 문제) 아래 5개 블록을 **하나씩 순서대로** 실행.

### 블록 1 — 테스트

```javascript
1+1
```
> 기대값: `2`. 콘솔 정상 작동 확인용.

---

### 블록 2 — Nonce 발급

```javascript
fetch("/wp-admin/admin-ajax.php?action=rest-nonce", {credentials: "include"})
  .then(r => r.text())
  .then(t => { window._nc = t.trim(); console.log("nonce ok:", window._nc.slice(0,8)); });
```
> 기대: `nonce ok: a1b2c3d4`

---

### 블록 3 — raw GET 저장

```javascript
fetch("/wp-json/wp/v2/pages/303?context=edit", {
  headers: {"X-WP-Nonce": window._nc},
  credentials: "include",
  cache: "no-store"
}).then(r => r.json()).then(p => {
  window._raw = p.content.raw;
  console.log("raw ok:", window._raw.length);
});
```
> 기대: `raw ok: 85XXX` (8만자 이상)

---

### 블록 4 — replace + PATCH

```javascript
let r = window._raw;
const cA = (r.match(/var sec=5;/g)||[]).length;
if (cA === 1) { r = r.replace("var sec=5;", "var sec=15;"); console.log("A ok"); }
else console.warn("A skip:", cA);

const ai = r.indexOf("||(isAI?480:800);card.classList.add");
if (ai !== -1) {
  const seg = r.slice(ai, ai+500);
  const OI = "setTimeout(function(){if(typeof onComplete";
  const NI = "setTimeout(function(){BH_hideOverlay();if(typeof onComplete";
  if (seg.includes(OI)) {
    r = r.slice(0,ai) + r.slice(ai).replace(OI, NI);
    console.log("B ok");
  } else { console.warn("B skip already"); }
} else { console.warn("B anchor miss"); }
window._patched = r;

fetch("/wp-json/wp/v2/pages/303", {
  method: "POST",
  headers: {"X-WP-Nonce": window._nc, "Content-Type": "application/json"},
  credentials: "include",
  body: JSON.stringify({content: window._patched})
}).then(r2 => r2.json()).then(j => console.log("patch ok id:", j.id));
```
> 기대: `A ok`, `B ok`, `patch ok id: 303`

---

### 블록 5 — 검증

```javascript
fetch("/wp-json/wp/v2/pages/303?context=edit", {
  headers: {"X-WP-Nonce": window._nc}, credentials: "include", cache: "no-store"
}).then(r => r.json()).then(p => {
  const v = p.content.raw;
  console.log("sec=15:", v.includes("var sec=15;") ? "PASS" : "FAIL");
  console.log("sec=5 gone:", !v.includes("var sec=5;") ? "PASS" : "FAIL");
  console.log("hideOverlay:", v.includes("BH_hideOverlay();if(typeof onComplete") ? "PASS" : "FAIL");
  console.log("len:", v.length);
});
```
> 기대: 3줄 모두 PASS

---

## 진단 명령어 — 어디서 막혔는지 확인

### 게임 로드 확인
```javascript
typeof BH_startWithDiff
```
> `"function"` 이면 정상 로드. `"undefined"` 이면 SyntaxError 있음.

### sec 변수 현재 라이브 패턴 확인
```javascript
fetch("/wp-admin/admin-ajax.php?action=rest-nonce",{credentials:"include"})
  .then(r=>r.text())
  .then(nc=>{
    return fetch("/wp-json/wp/v2/pages/303?context=edit",{
      headers:{"X-WP-Nonce":nc.trim()},credentials:"include",cache:"no-store"
    });
  }).then(r=>r.json()).then(p=>{
    const raw=p.content.raw;
    const i=raw.indexOf("BH_startAutoTimer");
    console.log(i!==-1 ? raw.slice(i,i+200) : "func not found");
    const i2=raw.indexOf("var sec=");
    console.log(i2!==-1 ? "sec pattern:"+raw.slice(i2,i2+30) : "sec not found");
  });
```

### Bug B anchor 확인
```javascript
fetch("/wp-admin/admin-ajax.php?action=rest-nonce",{credentials:"include"})
  .then(r=>r.text())
  .then(nc=>{
    return fetch("/wp-json/wp/v2/pages/303?context=edit",{
      headers:{"X-WP-Nonce":nc.trim()},credentials:"include",cache:"no-store"
    });
  }).then(r=>r.json()).then(p=>{
    const raw=p.content.raw;
    const ai=raw.indexOf("||(isAI?480:800);card.classList.add");
    if(ai===-1){console.log("anchor NOT found");return;}
    console.log("anchor found at",ai,"->",raw.slice(ai+35,ai+120));
  });
```

---

## 기대 콘솔 출력 (메인 스니펫 정상 케이스)

```
[1] OK nonce: a1b2c3d4
[2] OK raw len: 85XXX
[3a] OK A patched
[3b] OK B patched
[4] OK PATCH id: 303
[5] sec=15: PASS
[5] sec=5 gone: PASS
[5] hideOverlay added: PASS
[5] raw len: 85XXX
[5] ALL: PASS
```

이미 v1에서 부분 적용된 경우:
```
[3a] SKIP A (already patched or pattern not found)
[3b] SKIP B (OLD pattern not found in window — already patched)
```
→ 둘 다 SKIP이고 검증 PASS면 이미 완료 상태.

---

## PATCH 후 수동 검증 (Ctrl+Shift+R 새로고침 후)

1. https://neuralcare.co.kr/brain-games/minwhatoo/ 접속
2. 난이도 모달 표시 → **15초** 카운트다운 확인 (이전: 5초)
3. [보통] 클릭 → 게임 시작
4. 첫 번째 카드 reveal 후 오버레이 자동 사라짐 확인
5. 콘솔: `typeof BH_startWithDiff` → `"function"` 확인
