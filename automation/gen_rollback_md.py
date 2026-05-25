import sys, base64, hashlib
sys.stdout.reconfigure(encoding='utf-8')

with open('automation/rollback_post7_977f2ac.html', encoding='utf-8') as f:
    content = f.read()

content_bytes = content.encode('utf-8')
b64 = base64.b64encode(content_bytes).decode('ascii')
sha256_short = hashlib.sha256(content_bytes).hexdigest()[:16]
total_chars = len(content)
b64_len = len(b64)
utf8_bytes = len(content_bytes)

# 4000자 단위 청크로 b64 분할
CHUNK = 4000
chunks = [b64[i:i+CHUNK] for i in range(0, len(b64), CHUNK)]

# b64 변수 조립 JS
b64_lines = []
b64_lines.append('  var _b = ""')
for c in chunks:
    b64_lines.append('    + "' + c + '"')
b64_lines.append('  ;')
b64_js = '\n'.join(b64_lines)

lo = total_chars - 100
hi = total_chars + 100

snippet_lines = [
    '(async function() {',
    '  // === [977f2ac 롤백] Page #303 위젯 전체 교체 ===',
    '  // 원본: git commit 977f2ac (FSM 통합 이전 안정 버전)',
    '  // 원본 문자수: ' + str(total_chars) + ' / UTF-8 바이트: ' + str(utf8_bytes) + ' / SHA-256앞16: ' + sha256_short,
    '',
    '  // STEP 1: nonce 발급',
    "  var nonceResp = await fetch('/wp-admin/admin-ajax.php?action=rest-nonce', {credentials:'include', cache:'no-store'});",
    '  var nonce = await nonceResp.text();',
    '  nonce = nonce.trim();',
    "  if (!nonce || nonce.length < 5) { console.error('[ROLLBACK] nonce 실패:', nonce); return; }",
    "  console.log('[ROLLBACK] nonce OK:', nonce.slice(0,8) + '...');",
    '',
    '  // STEP 2: base64 -> UTF-8 복원',
    b64_js,
    "  var _decoded = new TextDecoder('utf-8').decode(",
    "    Uint8Array.from(atob(_b.replace(/\\s/g, '')), function(c) { return c.charCodeAt(0); })",
    '  );',
    "  console.log('[ROLLBACK] 복원 문자수:', _decoded.length, '(기대: " + str(total_chars) + ")');",
    '  if (_decoded.length < ' + str(lo) + ' || _decoded.length > ' + str(hi) + ') {',
    "    console.error('[ROLLBACK] 복원 길이 불일치! 중단.'); return;",
    '  }',
    '',
    '  // STEP 3: PATCH Page #303',
    "  var patchResp = await fetch('/wp-json/wp/v2/pages/303', {",
    "    method: 'POST',",
    "    credentials: 'include',",
    '    headers: {',
    "      'Content-Type': 'application/json',",
    "      'X-WP-Nonce': nonce,",
    "      'X-HTTP-Method-Override': 'PATCH'",
    '    },',
    '    body: JSON.stringify({ content: _decoded })',
    '  });',
    "  console.log('[ROLLBACK] PATCH status:', patchResp.status);",
    '  if (patchResp.status !== 200) {',
    '    var err = await patchResp.text();',
    "    console.error('[ROLLBACK] 실패:', err.slice(0,300)); return;",
    '  }',
    '',
    '  // STEP 4: 검증',
    '  var patchData = await patchResp.json();',
    '  var raw = (patchData.content && patchData.content.raw) ? patchData.content.raw : "";',
    '  var rawLen = raw.length;',
    "  console.log('[ROLLBACK] 라이브 raw length:', rawLen, '(기대: " + str(total_chars) + " +-10)');",
    '  var checks = {',
    '    rawLenOK: Math.abs(rawLen - ' + str(total_chars) + ') <= 10,',
    "    noFSM: raw.indexOf('BH_animateCardReveal') === -1,",
    "    hasSec5: raw.indexOf('var sec = 5') !== -1 || raw.indexOf('var sec=5') !== -1",
    '  };',
    "  console.log('[ROLLBACK] 검증:', JSON.stringify(checks));",
    '  if (checks.rawLenOK && checks.noFSM && checks.hasSec5) {',
    "    console.log('[ROLLBACK] === 모든 검증 PASS 롤백 완료 ===');",
    '  } else {',
    "    console.warn('[ROLLBACK] === 검증 실패 항목 있음 확인 필요 ===');",
    '  }',
    '})();',
]
snippet = '\n'.join(snippet_lines)

md_lines = [
    '# Post #7 라이브 롤백 스니펫 — 977f2ac 시점',
    '',
    '**생성일**: 2026-05-25',
    '**대상**: WP Page #303 (민화투 게임 허브)',
    '**롤백 목표**: commit 977f2ac (FSM 통합 이전 안정 버전)',
    '**정본 파일**: `automation/rollback_post7_977f2ac.html` (참조용 — 수정 금지)',
    '',
    '---',
    '',
    '## 사전 검증 결과 (git show 977f2ac 추출본 기준)',
    '',
    '| 항목 | 결과 |',
    '|---|---|',
    '| 원본 문자수 | ' + str(total_chars) + ' |',
    '| UTF-8 바이트 | ' + str(utf8_bytes) + ' |',
    '| base64 길이 | ' + str(b64_len) + ' |',
    '| SHA-256 앞16 | `' + sha256_short + '` |',
    '| wp:html 오픈 마커 | PASS (첫 줄: `<!-- wp:html -->`) |',
    '| wp:html 닫기 마커 | PASS (마지막 줄: `<!-- /wp:html -->`) |',
    '| style 내부 줄바꿈 | 0건 (wpautop 안전) |',
    '| script 내부 줄바꿈 | 0건 (wpautop 안전) |',
    '| JS 이모지 직접 문자 | 0건 |',
    '| BH_animateCardReveal 존재 | False (FSM 미포함 확인) |',
    '| sec= 기본값 | 5 |',
    '| BH_startWithDiff 존재 | True |',
    '',
    '---',
    '',
    '## 사용자 콘솔 실행 안내',
    '',
    '1. 브라우저에서 WP 관리자 로그인 상태 확인 (https://neuralcare.co.kr/wp-admin/)',
    '2. 개발자 도구 콘솔 열기 (F12 또는 Ctrl+Shift+J)',
    '3. 아래 스니펫 전체 복사 후 콘솔에 붙여넣기 후 Enter',
    '',
    '`[ROLLBACK] === 모든 검증 PASS 롤백 완료 ===` 메시지 출력 시 완료.',
    '',
    '---',
    '',
    '## PATCH 스니펫 (콘솔 1회 실행용)',
    '',
    '```javascript',
    snippet,
    '```',
    '',
    '---',
    '',
    '## PATCH 후 안전 검증 항목 3종',
    '',
    '| # | 항목 | 확인 방법 | 기대값 |',
    '|---|---|---|---|',
    '| 1 | raw length 일치 | 콘솔 `[ROLLBACK] 라이브 raw length` | ' + str(total_chars) + ' ±10 |',
    '| 2 | FSM 코드 0건 | 콘솔 checks `noFSM: true` | true |',
    '| 3 | sec=5 기본값 | 콘솔 checks `hasSec5: true` | true |',
    '',
    '---',
    '',
    '## 절대 금지',
    '',
    '- 정본 파일(`widgets/post7_widget.html`) 수정 금지 — git 보존',
    '- git 작업 금지 — 라이브만 롤백',
    '- 사용자 승인 없이 dev가 직접 PATCH 금지',
]
md_content = '\n'.join(md_lines)

with open('automation/wp_rollback_post7_977f2ac.md', 'w', encoding='utf-8') as f:
    f.write(md_content)

print('완료')
print('md 파일 크기:', len(md_content), '자')
print('스니펫 줄 수:', snippet.count('\n') + 1)
