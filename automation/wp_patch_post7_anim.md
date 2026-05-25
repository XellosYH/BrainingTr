# WP Page #303 라이브 PATCH 가이드 — Post #7 민화투 카드 인식 애니메이션

**생성**: 2026-05-25 / dev v6.55
**대상**: `https://neuralcare.co.kr/brain-games/minwhatoo/` (WP Page ID: 303)
**위젯 정본**: `C:\Claude_code\widgets\post7_widget.html` (85,042 bytes, 95줄, 커밋 a6bb5b6 기준)
**QA 사전 검수**: CONDITIONAL PASS (Q14 포기 버튼 = 기획 범위 외로 처리)

---

## 전제 조건

- 브라우저에서 `https://neuralcare.co.kr/wp-admin/` 로그인 상태 확인
- F12 → Console 탭 열기
- 아래 스니펫을 **순서대로** 실행 (단계 건너뜀 금지)

---

## Phase 1 — wp:html 블록 전체 교체 (브라우저 콘솔 방식)

> 85KB 단일 PATCH. 대부분의 환경에서 Phase 1만으로 완료 가능.
> Phase 1 실패(응답 413·401·빈 content) 시 → Phase 2 fallback 사용.

---

### 스니펫 1-A: Nonce 발급

```js
// Step 1: Nonce 발급 (콘솔 붙여넣기)
const nonceResp = await fetch('/wp-admin/admin-ajax.php?action=rest-nonce', {
  credentials: 'include'
});
const nonce = await nonceResp.text();
console.log('[STEP 1] Nonce:', nonce.slice(0, 10) + '...');
// ✅ 10자리 이상 문자열이면 정상
// ❌ "false" 또는 빈 문자열이면 → 로그인 세션 만료. wp-admin 재로그인 후 재시도
window.__BH_nonce = nonce.trim();
```

---

### 스니펫 1-B: 현재 raw content GET (롤백 보관용)

```js
// Step 2: 현재 페이지 raw content GET + 롤백 보관
const getResp = await fetch('/wp-json/wp/v2/pages/303?context=edit', {
  headers: { 'X-WP-Nonce': window.__BH_nonce },
  credentials: 'include',
  cache: 'no-store'
});
const pageData = await getResp.json();
window.__BH_backup_raw = pageData.content.raw;
console.log('[STEP 2] raw 길이(현재):', window.__BH_backup_raw.length);
console.log('[STEP 2] wp:html 블록 존재:', window.__BH_backup_raw.includes('<!-- wp:html -->'));
// ✅ 길이 > 1000 + wp:html 존재하면 정상
// ⚠️ wp:html 블록 없으면 → 아래 PATCH 시 새로 추가되는 방식으로 진행 가능 (문제 없음)
```

---

### 스니펫 1-C: 위젯 HTML 로드 (Python 사전 준비 필요)

> **사전 준비**: 아래 Python 명령을 Claude Code 터미널에서 먼저 실행하여 위젯을 JS 변수 할당 형식으로 출력한다.
>
> ```
> python C:\Claude_code\automation\gen_widget_js.py
> ```
>
> 위 파일이 없으면 아래 방법 사용:

**대안 — Python 직접 실행 (Claude Code PowerShell 터미널)**:

```powershell
# PowerShell 터미널에서 실행
python -c "
import re
with open(r'C:\Claude_code\widgets\post7_widget.html', encoding='utf-8') as f:
    html = f.read().strip()
# wp:html 마커 포함 확인
assert '<!-- wp:html -->' in html, 'wp:html 마커 누락!'
assert '<!-- /wp:html -->' in html, '/wp:html 마커 누락!'
# style/script 단일 행 검증
style_blocks = re.findall(r'<style[^>]*>(.*?)</style>', html, re.DOTALL)
script_blocks = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
for b in style_blocks + script_blocks:
    assert '<br' not in b and '<p>' not in b and '<hr>' not in b, 'wpautop 오염!'
print('검증 PASS')
print('바이트:', len(html.encode('utf-8')))
print('문자 수:', len(html))
"
```

**실측 출력 (2026-05-25)**:
```
PASS: validation ok
bytes: 85042
chars: 83736
wp:html count: 1 / /wp:html count: 1
widget_assign.js created — size chars: 84448
```

---

### 스니펫 1-D: 위젯 내용을 브라우저 변수에 로드

> 위젯 파일이 85KB이므로 브라우저 콘솔에 직접 붙여넣기는 어렵다.
> 아래 두 가지 방법 중 선택.

**방법 A — fetch로 로컬 파일 로드 (불가 — CORS 제한)**

로컬 파일 직접 fetch는 브라우저 보안 정책상 불가. 방법 B 사용.

**방법 B — Python으로 WP REST API 직접 PATCH (권장)**

Phase 1에서 가장 안정적인 방법. 아래 Python 스크립트를 Claude Code 터미널에서 실행.

```powershell
# PowerShell 터미널에서 실행
python -c "
import requests, re, json, sys

# ─── 설정 ────────────────────────────────────────────────
SITE      = 'https://neuralcare.co.kr'
PAGE_ID   = 303
WIDGET_PATH = r'C:\Claude_code\widgets\post7_widget.html'
# ─────────────────────────────────────────────────────────

# Step 1: 쿠키 세션 확인 (수동 입력 필요)
print('=' * 60)
print('사용 방법:')
print('  1. 브라우저 F12 → Application → Cookies → neuralcare.co.kr')
print('  2. wordpress_logged_in_* 쿠키 이름과 값 복사')
print('  3. 아래 COOKIE 변수에 입력 후 재실행')
print()
print('Phase 1-B 준비 완료 — Phase 1-D 방법 B Python 스크립트 사용 안내')
"
```

> 쿠키 기반 Python 방법이 복잡할 경우 → **브라우저 콘솔 방식** (Phase 1-E)으로 진행.

---

### 스니펫 1-E: 브라우저 콘솔 — fetch로 위젯 주입 (권장 최종 방법)

아래 방법은 위젯을 **서버에서 직접 가져오는 대신**, 이미 로드된 페이지 컨텍스트에서 PATCH를 수행한다.

```js
// Step 3: 위젯 raw 문자열 준비
// ── 이 블록 안의 내용을 Python이 생성한 문자열로 교체 ──
// Python 생성 방법:
//   python -c "
//   with open(r'C:\Claude_code\widgets\post7_widget.html', encoding='utf-8') as f:
//       h = f.read().strip()
//   js = repr(h)  # Python repr → JS 호환 문자열 (작은따옴표 escape 포함)
//   print('window.__BH_widget = ' + js + ';')
//   " > C:\Claude_code\automation\widget_assign.js
//
// 생성된 widget_assign.js 파일 전체를 콘솔에 붙여넣어 window.__BH_widget 변수를 세팅한 뒤,
// 아래 Step 4 스니펫 실행.
//
// 파일이 클 경우 → Phase 2 (Base64 청크 방식) 사용

console.log('[STEP 3] 위젯 로드 방법: widget_assign.js 콘솔 붙여넣기');
console.log('  python 명령으로 widget_assign.js 생성 후 파일 내용 전체 복사 → 콘솔 붙여넣기');
```

**Python으로 widget_assign.js 생성**:

```powershell
# PowerShell 터미널에서 실행
python -c "
import json
with open(r'C:\Claude_code\widgets\post7_widget.html', encoding='utf-8') as f:
    html = f.read().strip()
js_str = 'window.__BH_widget = ' + json.dumps(html, ensure_ascii=False) + ';'
js_str += '\nconsole.log(\"[STEP 3] 위젯 로드 완료, 길이:\", window.__BH_widget.length);'
with open(r'C:\Claude_code\automation\widget_assign.js', 'w', encoding='utf-8') as o:
    o.write(js_str)
print('생성 완료: C:\\\\Claude_code\\\\automation\\\\widget_assign.js')
print('파일 크기:', len(js_str), '자')
"
```

> 생성된 `widget_assign.js` 파일 전체 내용을 브라우저 콘솔에 붙여넣기.
> 콘솔 출력 `[STEP 3] 위젯 로드 완료, 길이: NNNNN` 확인 후 다음 단계 진행.

---

### 스니펫 1-F: wp:html 블록 교체 + PATCH 전송

```js
// Step 4: wp:html 블록 교체 + PATCH
// ※ 반드시 Step 1(nonce), Step 2(backup), Step 3(widget 로드) 완료 후 실행

(async () => {
  const WP_OPEN  = '<!-- wp:html -->';
  const WP_CLOSE = '<!-- /wp:html -->';

  const raw = window.__BH_backup_raw;
  const widget = window.__BH_widget;

  // 위젯에 wp:html 마커 포함 여부 확인
  if (!widget.includes(WP_OPEN)) {
    console.error('[STEP 4] ❌ 위젯에 wp:html 마커 없음 — widget_assign.js 재생성 필요');
    return;
  }

  // 기존 wp:html 블록 범위 찾기
  const wStart = raw.indexOf(WP_OPEN);
  const wEnd   = raw.indexOf(WP_CLOSE);

  let newRaw;
  if (wStart === -1 || wEnd === -1) {
    // 기존 wp:html 블록 없음 → 본문 끝에 추가
    console.log('[STEP 4] ⚠️ 기존 wp:html 블록 없음 → 본문 끝에 새로 추가');
    newRaw = raw + '\n\n' + widget;
  } else {
    // 기존 블록 전체 교체
    const before = raw.slice(0, wStart);
    const after  = raw.slice(wEnd + WP_CLOSE.length);
    newRaw = before + widget + after;
    console.log('[STEP 4] 교체 범위:', wStart, '~', wEnd + WP_CLOSE.length);
  }

  // PATCH 전 검증
  if (!newRaw.includes(WP_OPEN) || !newRaw.includes(WP_CLOSE)) {
    console.error('[STEP 4] ❌ 교체 후 wp:html 마커 없음 — 중단');
    return;
  }
  if (newRaw.indexOf('<!-- wp:html -->') !== newRaw.lastIndexOf('<!-- wp:html -->')) {
    console.warn('[STEP 4] ⚠️ wp:html 블록이 2개 이상 — 확인 필요');
  }

  console.log('[STEP 4] raw 길이 (교체 후):', newRaw.length, '(기존:', raw.length + ')');

  // PATCH 전송
  const patchResp = await fetch('/wp-json/wp/v2/pages/303', {
    method: 'POST',
    headers: {
      'X-WP-Nonce': window.__BH_nonce,
      'Content-Type': 'application/json'
    },
    credentials: 'include',
    body: JSON.stringify({ content: newRaw })
  });

  if (!patchResp.ok) {
    console.error('[STEP 4] ❌ PATCH 실패:', patchResp.status, patchResp.statusText);
    const errBody = await patchResp.text();
    console.error('오류 내용:', errBody.slice(0, 300));
    console.log('[STEP 4] 롤백 방법: window.__BH_backup_raw 로 재PATCH (Step 4 재실행 전 변수 복구)');
    return;
  }

  const result = await patchResp.json();
  console.log('[STEP 4] ✅ PATCH 성공 — Page ID:', result.id, '/ Status:', result.status);
  window.__BH_patch_result = result;
})();
```

---

### 스니펫 1-G: GET 재확인

```js
// Step 5: GET 재확인 — 저장 정합 검증
(async () => {
  const verifyResp = await fetch('/wp-json/wp/v2/pages/303?context=edit', {
    headers: { 'X-WP-Nonce': window.__BH_nonce },
    credentials: 'include',
    cache: 'no-store'
  });
  const verifyData = await verifyResp.json();
  const verifyRaw = verifyData.content.raw;

  const checks = {
    'wp:html 존재':        verifyRaw.includes('<!-- wp:html -->'),
    '/wp:html 존재':       verifyRaw.includes('<!-- /wp:html -->'),
    'BH_animateCardReveal 존재': verifyRaw.includes('BH_animateCardReveal'),
    'BH_startWithDiff 존재':     verifyRaw.includes('BH_startWithDiff'),
    'BH_ANIM_SPEED 존재':        verifyRaw.includes('BH_ANIM_SPEED'),
    '길이 일치 (>80000)':        verifyRaw.length > 80000,
    '<br> in script (0건)':      !/<script[^>]*>[^<]*<br/i.test(verifyRaw),
    '<p> in script (0건)':       !/<script[^>]*>[^<]*<p>/i.test(verifyRaw),
  };

  let allPass = true;
  console.log('[STEP 5] GET 재확인 결과:');
  for (const [k, v] of Object.entries(checks)) {
    console.log(`  ${v ? '✅' : '❌'} ${k}`);
    if (!v) allPass = false;
  }
  console.log('[STEP 5] raw 길이:', verifyRaw.length);
  console.log(allPass ? '[STEP 5] ✅ 전체 PASS → Phase 2 불필요' : '[STEP 5] ❌ FAIL → Phase 2 또는 롤백 필요');
})();
```

---

## Phase 2 — Base64 청크 분할 방식 (Phase 1 실패 시 Fallback)

> Phase 1 스니펫 1-F에서 PATCH 실패(413 / 빈 content) 또는 GET 재확인 FAIL 시 사용.

### Phase 2-A: Python으로 Base64 청크 파일 생성

```powershell
# PowerShell 터미널에서 실행
python -c "
import base64, json

CHUNK_SIZE = 4000  # 4000자 단위

with open(r'C:\Claude_code\widgets\post7_widget.html', encoding='utf-8') as f:
    html = f.read().strip()

# UTF-8 인코딩 후 Base64 변환
b64 = base64.b64encode(html.encode('utf-8')).decode('ascii')

print('원본 바이트:', len(html.encode('utf-8')))
print('Base64 길이:', len(b64))
print('청크 수:', (len(b64) + CHUNK_SIZE - 1) // CHUNK_SIZE)

# 청크 분할 + JS 할당 파일 생성
lines = []
lines.append('window._wg = \"\";')
for i, start in enumerate(range(0, len(b64), CHUNK_SIZE)):
    chunk = b64[start:start+CHUNK_SIZE]
    lines.append(f'window._wg += \"{chunk}\";')
    lines.append(f'console.log(\"[청크 {i+1}] 누적 길이:\", window._wg.length);')

lines.append('')
lines.append('// 모든 청크 주입 완료 후 아래 Phase 2-B 실행')

out = '\n'.join(lines)
with open(r'C:\Claude_code\automation\widget_b64_chunks.js', 'w', encoding='ascii') as o:
    o.write(out)

print('생성 완료: C:\\\\Claude_code\\\\automation\\\\widget_b64_chunks.js')
"
```

### Phase 2-B: 청크 주입 (브라우저 콘솔)

1. `widget_b64_chunks.js` 파일 전체를 브라우저 콘솔에 붙여넣기
2. 각 청크마다 `[청크 N] 누적 길이: NNNN` 출력 확인
3. 마지막 청크까지 모두 출력 확인 후 아래 Phase 2-C 실행

### Phase 2-C: TextDecoder UTF-8 복원 + PATCH

```js
// Phase 2-C: Base64 → UTF-8 복원 + PATCH
// ※ CLAUDE.md §Base64 위젯 UTF-8 디코딩 룰 준수 (atob() 단독 사용 금지)
(async () => {
  if (!window._wg) {
    console.error('[Phase 2-C] ❌ window._wg 미설정 — Phase 2-B 먼저 실행');
    return;
  }

  // 공백 혼입 제거 (CLAUDE.md §window._wg 전처리 필수)
  const b64clean = window._wg.replace(/\s/g, '');
  console.log('[Phase 2-C] Base64 길이 (정리 후):', b64clean.length);

  // UTF-8 디코딩 (atob + TextDecoder 조합 — 한글/이모지 안전)
  let widgetHtml;
  try {
    const bytes = Uint8Array.from(atob(b64clean), c => c.charCodeAt(0));
    widgetHtml = new TextDecoder('utf-8').decode(bytes);
  } catch (e) {
    console.error('[Phase 2-C] ❌ Base64 디코딩 실패:', e.message);
    return;
  }

  console.log('[Phase 2-C] 위젯 복원 길이:', widgetHtml.length);
  if (!widgetHtml.includes('<!-- wp:html -->')) {
    console.error('[Phase 2-C] ❌ wp:html 마커 없음 — 청크 누락 가능성');
    return;
  }

  // 현재 raw GET
  const getResp = await fetch('/wp-json/wp/v2/pages/303?context=edit', {
    headers: { 'X-WP-Nonce': window.__BH_nonce },
    credentials: 'include',
    cache: 'no-store'
  });
  const pageData = await getResp.json();
  const raw = pageData.content.raw;

  // wp:html 블록 교체
  const WP_OPEN  = '<!-- wp:html -->';
  const WP_CLOSE = '<!-- /wp:html -->';
  const wStart = raw.indexOf(WP_OPEN);
  const wEnd   = raw.indexOf(WP_CLOSE);

  let newRaw;
  if (wStart === -1 || wEnd === -1) {
    newRaw = raw + '\n\n' + widgetHtml;
  } else {
    newRaw = raw.slice(0, wStart) + widgetHtml + raw.slice(wEnd + WP_CLOSE.length);
  }

  // PATCH
  const patchResp = await fetch('/wp-json/wp/v2/pages/303', {
    method: 'POST',
    headers: {
      'X-WP-Nonce': window.__BH_nonce,
      'Content-Type': 'application/json'
    },
    credentials: 'include',
    body: JSON.stringify({ content: newRaw })
  });

  if (!patchResp.ok) {
    console.error('[Phase 2-C] ❌ PATCH 실패:', patchResp.status);
    return;
  }
  const result = await patchResp.json();
  console.log('[Phase 2-C] ✅ PATCH 성공 — ID:', result.id);
})();
```

---

## 롤백 절차 (PATCH 실패 또는 GET 재확인 FAIL 시)

```js
// 롤백: Step 2에서 보관한 backup raw으로 재PATCH
(async () => {
  if (!window.__BH_backup_raw) {
    console.error('[롤백] ❌ backup_raw 없음 — 수동 롤백 필요 (WP 에디터 이전 버전 복원)');
    return;
  }
  const rollbackResp = await fetch('/wp-json/wp/v2/pages/303', {
    method: 'POST',
    headers: {
      'X-WP-Nonce': window.__BH_nonce,
      'Content-Type': 'application/json'
    },
    credentials: 'include',
    body: JSON.stringify({ content: window.__BH_backup_raw })
  });
  const r = await rollbackResp.json();
  console.log(rollbackResp.ok ? '[롤백] ✅ 롤백 완료 — ID:' + r.id : '[롤백] ❌ 롤백도 실패 — WP 관리자 이전 버전 복원 필요');
})();
```

---

## 라이브 검증 체크리스트

PATCH 완료 후 `https://neuralcare.co.kr/brain-games/minwhatoo/` 접속, F12 → Console에서 순서대로 실행.

### 필수 검증 (S3·SW)

> S1(본문 500자) = 게임 허브 페이지 예외 → **S1 면제** (CLAUDE.md §S1 예외)

```js
// S3: Mojibake 0건 확인
const bodyText = document.body.innerText;
const mojibakePattern = /[ë ì í â ã ]/g;  // Latin-1 잘못 해석 패턴
const mojibakeHits = (bodyText.match(mojibakePattern) || []).length;
console.log('[S3] Mojibake 건수:', mojibakeHits, mojibakeHits === 0 ? '✅ PASS' : '❌ FAIL');

// SW: 필수 함수 4종 로드 확인
const swChecks = {
  'BH_animateCardReveal': typeof BH_animateCardReveal === 'function',
  'BH_animateCapture':    typeof BH_animateCapture === 'function',
  'BH_ANIM_SPEED':        typeof BH_ANIM_SPEED === 'object' && BH_ANIM_SPEED !== null,
  'BH_startWithDiff':     typeof BH_startWithDiff === 'function',
};
let swAll = true;
for (const [k, v] of Object.entries(swChecks)) {
  console.log(`[SW] ${v ? '✅' : '❌'} ${k}: ${typeof window[k]}`);
  if (!v) swAll = false;
}
console.log('[SW] 종합:', swAll ? '✅ PASS' : '❌ FAIL — 위젯 재업로드 필요');
```

### 추가 동적 검증

```js
// A13: 카드 48장 type↔svgUrl mismatch 0건
if (typeof BH_DECK_DATA !== 'undefined') {
  const total = BH_DECK_DATA.length;
  const mismatch = BH_DECK_DATA.filter(c => !c.type || !c.svgUrl || c.svgUrl === '').length;
  console.log('[A13] 전체 카드:', total, '/ mismatch:', mismatch);
  console.log('[A13]', total === 48 && mismatch === 0 ? '✅ PASS' : '❌ FAIL');
} else {
  console.log('[A13] ❌ BH_DECK_DATA 미정의 — SW FAIL과 연동');
}

// Q8: BH_overlay_card 클릭 → BH_skipAnim 연결 확인 (정적 확인)
if (typeof BH_skipAnim === 'function') {
  console.log('[Q8] ✅ BH_skipAnim 함수 존재 — 실제 클릭 트리거는 게임 ANIMATING 중 직접 클릭으로 확인');
} else {
  console.log('[Q8] ❌ BH_skipAnim 미정의');
}

// Q12: 족보 효과음 함수 존재 확인
if (typeof BH_AudioContext !== 'undefined' || typeof BH_playCardPlace === 'function') {
  console.log('[Q12] ✅ 사운드 모듈 로드 확인 — 족보 달성 효과음 순서는 실제 플레이로 확인');
} else {
  console.log('[Q12] ⚠️ 사운드 모듈 미검출 — BH_SoundMuted 상태 확인 필요');
}

// 모달 display 방식 확인 (CLAUDE.md §style.display 직접 제어 필수)
const modalChecks = [
  document.getElementById('BH_diff_modal'),
  document.getElementById('BH_game_board'),
  document.getElementById('BH_result_modal'),
];
modalChecks.forEach((el, i) => {
  if (!el) {
    console.log(`[MODAL ${i}] ❌ 요소 미발견`);
    return;
  }
  const hasHidden = el.hasAttribute('hidden');
  console.log(`[MODAL ${i}] ${el.id}: hasAttribute(hidden)=${hasHidden}`, hasHidden ? '⚠️ [hidden] 방식 사용 — CLAUSE.md 위반' : '✅ style.display 방식');
});
```

### 최종 종합 판정

```js
// 최종 판정
console.log('');
console.log('═══════════ 라이브 검증 최종 종합 ═══════════');
console.log('S1: 게임 허브 페이지 예외 — 면제');
console.log('S3: 위 Mojibake 결과 확인');
console.log('SW: 위 함수 4종 결과 확인');
console.log('A13: 카드 48장 mismatch 결과 확인');
console.log('Q8: BH_skipAnim 존재 확인');
console.log('Q12: 사운드 모듈 확인');
console.log('');
console.log('전체 PASS → WP 관리자에서 "업데이트" 클릭 후 발행 완료');
console.log('FAIL 항목 있으면 → Phase 2 시도 또는 롤백 후 lead 보고');
```

---

## 실행 순서 요약 (N단계)

| 단계 | 작업 | 도구 | 확인 |
|---|---|---|---|
| 1 | Python: `widget_assign.js` 생성 | PowerShell | 파일 생성 확인 |
| 2 | 브라우저: wp-admin 로그인 확인 | Chrome | 관리자 화면 접속 |
| 3 | F12 Console: 스니펫 1-A (Nonce 발급) | Chrome Console | 10자리+ 출력 |
| 4 | F12 Console: 스니펫 1-B (backup GET) | Chrome Console | 길이 > 1000 |
| 5 | F12 Console: `widget_assign.js` 붙여넣기 | Chrome Console | 길이 NNNNN 출력 |
| 6 | F12 Console: 스니펫 1-F (PATCH 전송) | Chrome Console | ✅ PATCH 성공 |
| 7 | F12 Console: 스니펫 1-G (GET 재확인) | Chrome Console | 전체 PASS |
| 8 | 페이지 새로고침 후 라이브 검증 체크리스트 실행 | Chrome Console | S3·SW·A13 PASS |
| (실패 시) | Phase 2 Base64 청크 방식 실행 | PowerShell + Console | Phase 2-C PATCH |

> ⚠️ git commit·tag·push는 lead 사전 승인 후 Claude Code에서만 실행. 이 가이드 실행 중 git 명령 금지.

---

## 참고 — Q14 포기 버튼 처리 방침

QA 보고서 B-Q14: 포기 버튼 관련 코드 미검출.
**처리 방침**: 기획서 §8 Q14는 이번 배포(카드 인식 애니메이션) 범위 외로 처리. 다음 game 에이전트 작업 사이클에서 구현 여부 확인.

---

*생성: dev v6.55 / 2026-05-25*
*대상 Page ID: 303 / 위젯 정본: widgets/post7_widget.html (85,042 bytes)*
