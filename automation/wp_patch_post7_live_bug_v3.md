# WP Page #303 Live Target PATCH Snippet v3
**Author**: dev v6.55 / 2026-05-25
**Target**: https://neuralcare.co.kr/brain-games/minwhatoo/ (WP Page ID: 303)
**Purpose**: PATCH C (BH_initGame phase reset) + PATCH D (BH_doAITurn phase guard)
**Base**: v2 snippet pattern (no Korean, no single quotes)

---

## Anchor Verification (pre-write grep results)

| Item | Pattern | Count in post7_widget.html | Status |
|---|---|---|---|
| PATCH C old | `BH_GS.difficulty=diff\|\|'normal';var shuffled=BH_shuffle` | 1 | OK unique |
| PATCH D old | `function BH_doAITurn(){if(BH_GS.aiHand.length===0)` | 1 | OK unique |
| PATCH C new (already applied?) | `BH_GS.phase='IDLE';BH_GS.animStage='IDLE'` | 0 | NOT YET |
| PATCH D new (already applied?) | `BH_GS.phase!=='AI_TURN')return` | 0 | NOT YET |

**Conclusion**: Both patches needed in canonical file. Live WP may also be un-patched.

---

## What Changed vs v2

| Version | Patches |
|---|---|
| v2 | Bug A (sec=5->15) + Bug B (hideOverlay insert) |
| **v3** | **Bug A skip + Bug B skip + PATCH C + PATCH D** |

v3 executes SKIP-safe for A and B (already applied in canonical file),
then applies C and D which are not yet in live WP.

---

## Main Snippet v3 (no Korean, no single quotes)

> Prerequisites: WP admin logged in. neuralcare.co.kr tab open.
> All string literals use double quotes `"` only. Zero Korean characters. Zero single quotes.

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

  // Pre-check: confirm v2 patches (A and B) are already applied
  const preA = raw.includes("var sec=15;");
  const preB = raw.includes("BH_hideOverlay();if(typeof onComplete");
  console.log("[pre] sec=15 (v2A):", preA ? "OK" : "MISSING - run v2 first");
  console.log("[pre] hideOverlay (v2B):", preB ? "OK" : "MISSING - run v2 first");
  if (!preA || !preB) {
    console.error("[pre] ABORT - v2 patches not yet applied to live WP. Run v2 snippet first.");
    return;
  }

  // PATCH C: BH_initGame - add phase/animStage reset
  const OLD_C = "BH_GS.difficulty=diff||\"normal\";var shuffled=BH_shuffle(BH_DECK_DATA);";
  const NEW_C = "BH_GS.difficulty=diff||\"normal\";BH_GS.phase=\"IDLE\";BH_GS.animStage=\"IDLE\";var shuffled=BH_shuffle(BH_DECK_DATA);";
  const cntC = (raw.match(/BH_GS\.difficulty=diff\|\|"normal";var shuffled=BH_shuffle\(BH_DECK_DATA\);/g) || []).length;
  if (cntC === 0) {
    console.warn("[3c] SKIP C (already patched or pattern not found)");
  } else if (cntC > 1) {
    console.error("[3c] FAIL C duplicates:", cntC);
    return;
  } else {
    raw = raw.replace(OLD_C, NEW_C);
    console.log("[3c] OK C patched");
  }

  // PATCH D: BH_doAITurn - add phase guard
  const OLD_D = "function BH_doAITurn(){if(BH_GS.aiHand.length===0){if(BH_checkGameOver()){BH_showResults();}else{BH_setPhase(\"PLAYER_TURN\");BH_renderBoard();}return;}";
  const NEW_D = "function BH_doAITurn(){if(BH_GS.phase!==\"AI_TURN\")return;if(BH_GS.aiHand.length===0){if(BH_checkGameOver()){BH_showResults();}else{BH_setPhase(\"PLAYER_TURN\");BH_renderBoard();}return;}";
  const cntD = (raw.match(/function BH_doAITurn\(\)\{if\(BH_GS\.aiHand\.length===0\)\{if\(BH_checkGameOver\(\)\)\{BH_showResults\(\);\}else\{BH_setPhase\("PLAYER_TURN"\);BH_renderBoard\(\);\}return;\}/g) || []).length;
  if (cntD === 0) {
    console.warn("[3d] SKIP D (already patched or pattern not found)");
  } else if (cntD > 1) {
    console.error("[3d] FAIL D duplicates:", cntD);
    return;
  } else {
    raw = raw.replace(OLD_D, NEW_D);
    console.log("[3d] OK D patched");
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

  const r1 = vraw.includes("BH_GS.phase=\"IDLE\";BH_GS.animStage=\"IDLE\"");
  const r2 = !vraw.includes("BH_GS.difficulty=diff||\"normal\";var shuffled=BH_shuffle(BH_DECK_DATA);") || r1;
  const r3 = vraw.includes("BH_GS.phase!=\"=AI_TURN\")return");
  const r3b = vraw.includes("!=\"\"AI_TURN\")return") || vraw.includes("!="AI_TURN")return");
  // robust check: look for the guard in doAITurn
  const doAIIdx = vraw.indexOf("function BH_doAITurn()");
  const doAISegment = doAIIdx !== -1 ? vraw.slice(doAIIdx, doAIIdx + 80) : "";
  const r3c = doAISegment.includes("AI_TURN") && doAISegment.includes("return");
  console.log("[5] phase IDLE in initGame:", r1 ? "PASS" : "FAIL");
  console.log("[5] doAITurn phase guard:", r3c ? "PASS" : "FAIL");
  console.log("[5] raw len:", vraw.length);
  console.log("[5] ALL:", (r1 && r3c) ? "PASS" : "FAIL - check above");
})();
```

---

## Fallback Split Execution (5 blocks)

If main snippet fails with SyntaxError, run blocks **one at a time in order**.

### Block 1 - Test

```javascript
1+1
```
> Expected: `2`

---

### Block 2 - Nonce

```javascript
fetch("/wp-admin/admin-ajax.php?action=rest-nonce", {credentials: "include"})
  .then(r => r.text())
  .then(t => { window._nc = t.trim(); console.log("nonce ok:", window._nc.slice(0,8)); });
```
> Expected: `nonce ok: a1b2c3d4`

---

### Block 3 - GET raw

```javascript
fetch("/wp-json/wp/v2/pages/303?context=edit", {
  headers: {"X-WP-Nonce": window._nc},
  credentials: "include",
  cache: "no-store"
}).then(r => r.json()).then(p => {
  window._raw = p.content.raw;
  console.log("raw ok:", window._raw.length);
  console.log("sec=15:", window._raw.includes("var sec=15;") ? "OK" : "MISSING");
  console.log("hideOverlay:", window._raw.includes("BH_hideOverlay();if(typeof onComplete") ? "OK" : "MISSING");
});
```
> Expected: `raw ok: 85XXX`, `sec=15: OK`, `hideOverlay: OK`
> If either is MISSING: run v2 snippet first before continuing.

---

### Block 4 - PATCH C + D

```javascript
let r = window._raw;

const OLD_C = "BH_GS.difficulty=diff||\"normal\";var shuffled=BH_shuffle(BH_DECK_DATA);";
const NEW_C = "BH_GS.difficulty=diff||\"normal\";BH_GS.phase=\"IDLE\";BH_GS.animStage=\"IDLE\";var shuffled=BH_shuffle(BH_DECK_DATA);";
const cC = (r.match(/BH_GS\.difficulty=diff\|\|"normal";var shuffled=BH_shuffle\(BH_DECK_DATA\);/g)||[]).length;
if (cC === 1) { r = r.replace(OLD_C, NEW_C); console.log("C ok"); }
else console.warn("C skip cC=", cC);

const OLD_D = "function BH_doAITurn(){if(BH_GS.aiHand.length===0){if(BH_checkGameOver()){BH_showResults();}else{BH_setPhase(\"PLAYER_TURN\");BH_renderBoard();}return;}";
const NEW_D = "function BH_doAITurn(){if(BH_GS.phase!=\"AI_TURN\")return;if(BH_GS.aiHand.length===0){if(BH_checkGameOver()){BH_showResults();}else{BH_setPhase(\"PLAYER_TURN\");BH_renderBoard();}return;}";
const cD = (r.match(/function BH_doAITurn\(\)\{if\(BH_GS\.aiHand\.length===0\)/g)||[]).length;
if (cD === 1) { r = r.replace(OLD_D, NEW_D); console.log("D ok"); }
else console.warn("D skip cD=", cD);

window._patched = r;
fetch("/wp-json/wp/v2/pages/303", {
  method: "POST",
  headers: {"X-WP-Nonce": window._nc, "Content-Type": "application/json"},
  credentials: "include",
  body: JSON.stringify({content: window._patched})
}).then(r2 => r2.json()).then(j => console.log("patch ok id:", j.id));
```
> Expected: `C ok`, `D ok`, `patch ok id: 303`

---

### Block 5 - Verify

```javascript
fetch("/wp-json/wp/v2/pages/303?context=edit", {
  headers: {"X-WP-Nonce": window._nc}, credentials: "include", cache: "no-store"
}).then(r => r.json()).then(p => {
  const v = p.content.raw;
  const doAIIdx = v.indexOf("function BH_doAITurn()");
  const doAISeg = doAIIdx !== -1 ? v.slice(doAIIdx, doAIIdx + 80) : "";
  console.log("C phase IDLE:", v.includes("BH_GS.phase=\"IDLE\";BH_GS.animStage=\"IDLE\"") ? "PASS" : "FAIL");
  console.log("D phase guard:", (doAISeg.includes("AI_TURN") && doAISeg.includes("return")) ? "PASS" : "FAIL");
  console.log("doAITurn head:", doAISeg);
  console.log("len:", v.length);
});
```
> Expected: both PASS. `doAITurn head` shows guard at start.

---

## Expected Console Output (normal case)

```
[1] OK nonce: a1b2c3d4
[2] OK raw len: 85XXX
[pre] sec=15 (v2A): OK
[pre] hideOverlay (v2B): OK
[3c] OK C patched
[3d] OK D patched
[4] OK PATCH id: 303
[5] phase IDLE in initGame: PASS
[5] doAITurn phase guard: PASS
[5] raw len: 85XXX
[5] ALL: PASS
```

If v2 patches not yet in live WP:
```
[pre] ABORT - v2 patches not yet applied to live WP. Run v2 snippet first.
```
-> Run v2 snippet first, then re-run v3.

---

## Post-PATCH Manual Verification

1. Open https://neuralcare.co.kr/brain-games/minwhatoo/
2. Hard refresh: Ctrl+Shift+R
3. Wait for difficulty modal
4. Click the difficulty button
5. Play 2-3 turns manually
6. Click new game (restart)
7. Verify: game does NOT auto-play after restart
8. Console check: `typeof BH_startWithDiff` -> `"function"`
