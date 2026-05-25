import sys, re

content = open('C:/Claude_code/widgets/post7_widget.html', encoding='utf-8').read()
lines = content.split('\n')

# ============================================================
# STEP 1: CSS 통합 (line 73, index 72)
# ============================================================
css_new = (
    '.BH_anim_base{will-change:transform,opacity !important;transform-origin:center center !important;'
    'backface-visibility:hidden !important;-webkit-backface-visibility:hidden !important;}'
    '.BH_anim_zoom{animation:BH_zoomIn 250ms cubic-bezier(0.34,1.56,0.64,1) forwards !important;}'
    '@keyframes BH_zoomIn{0%{transform:scale(1);}100%{transform:scale(1.18);}}'
    '.BH_anim_overlap{animation:BH_overlap 300ms ease-out forwards !important;}'
    '@keyframes BH_overlap{0%{transform:scale(1.18) translate(0,0);}100%{transform:scale(1.1) translate(30px,-30px);}}'
    '.BH_anim_move{animation:BH_flyToCapture 450ms ease-in forwards !important;}'
    '@keyframes BH_flyToCapture{'
    '0%{transform:scale(1.1) translate(30px,-30px);opacity:1;}'
    '40%{transform:scale(0.9) translate(30px,-30px);opacity:0.8;}'
    '100%{transform:scale(0.5) translate(30px,-30px);opacity:0;}}'
    '@media (prefers-reduced-motion:reduce){'
    '.BH_anim_base,.BH_anim_zoom,.BH_anim_overlap,.BH_anim_move{animation:none !important;transition:none !important;}}'
    '.BH_overlay_card{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%) scale(1);'
    'z-index:999;pointer-events:none;border-radius:8px;box-shadow:0 8px 32px rgba(0,0,0,0.4);}'
    '.BH_card_playing{opacity:0.5 !important;}'
)

old_css_line = lines[72]
assert old_css_line.endswith('}</style>'), 'CSS line does not end with }</style>'
new_css_line = old_css_line[:-len('</style>')] + css_new + '</style>'
print('CSS STEP1 OK. New CSS line:', len(new_css_line))

# ============================================================
# STEP 2: HTML 오버레이 컨테이너 추가
# ============================================================
old_gameboard_tag = 'id="BH_game_board" style="display:none">'
new_gameboard_tag = 'id="BH_game_board" style="display:none"><div class="BH_overlay_card" id="BH_overlay_card" style="display:none;"></div>'

# HTML은 라인 0~71 범위 내에 있음
html_section = '\n'.join(lines[:72])
assert old_gameboard_tag in html_section, 'gameboard tag not found'
new_html_section = html_section.replace(old_gameboard_tag, new_gameboard_tag, 1)
html_lines = new_html_section.split('\n')
print('HTML STEP2 OK. HTML lines:', len(html_lines))

# ============================================================
# STEP 3: Sound JS 삽입
# ============================================================
old_js_line = lines[73]
sound_minify = (
    'function BH_playReveal(){'
    'if(window.BH_SoundMuted)return;'
    'try{'
    'var ac=BH_getAC(),o=ac.createOscillator(),g=ac.createGain();'
    'o.connect(g);g.connect(ac.destination);'
    "o.type='sine';"
    'o.frequency.setValueAtTime(740,ac.currentTime);'
    'g.gain.setValueAtTime(0,ac.currentTime);'
    'g.gain.linearRampToValueAtTime(.13,ac.currentTime+.01);'
    'g.gain.exponentialRampToValueAtTime(.001,ac.currentTime+.22);'
    'o.start(ac.currentTime);o.stop(ac.currentTime+.22);'
    '}catch(e){}}'
    'function BH_playCapture(){'
    'if(window.BH_SoundMuted)return;'
    'try{'
    'var ac=BH_getAC(),o=ac.createOscillator(),g=ac.createGain();'
    'o.connect(g);g.connect(ac.destination);'
    "o.type='triangle';"
    'o.frequency.setValueAtTime(440,ac.currentTime);'
    'o.frequency.exponentialRampToValueAtTime(330,ac.currentTime+.24);'
    'g.gain.setValueAtTime(0,ac.currentTime);'
    'g.gain.linearRampToValueAtTime(.12,ac.currentTime+.008);'
    'g.gain.exponentialRampToValueAtTime(.001,ac.currentTime+.24);'
    'o.start(ac.currentTime);o.stop(ac.currentTime+.24);'
    '}catch(e){}}'
)

insert_sound_after = '};try{window.BH_SoundMuted'
assert insert_sound_after in old_js_line, 'sound insert marker not found'
new_js_line = old_js_line.replace(insert_sound_after, '}' + sound_minify + ';try{window.BH_SoundMuted', 1)
print('Sound STEP3 OK. JS delta:', len(new_js_line) - len(old_js_line))

# ============================================================
# STEP 4: 4개 애니메이션 함수 신설
# BH_initGame 직전에 삽입
# ============================================================
anim_functions = (
    'var BH_prefersReducedMotion=!!(window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches);'
    'function BH_supportsTransition(){return "transition" in document.documentElement.style||"webkitTransition" in document.documentElement.style;}'
    'var BH_ANIM_SPEED={slow:{zoom:400,pause:900,overlap:500,capture:700},normal:{zoom:250,pause:600,overlap:300,capture:450},fast:{zoom:150,pause:300,overlap:200,capture:250}};'
    'function BH_getAnimSpd(){try{return BH_ANIM_SPEED[localStorage.getItem("BH_animSpeed")||"normal"]||BH_ANIM_SPEED.normal;}catch(e){return BH_ANIM_SPEED.normal;}}'
    # BH_animZoom
    'function BH_animZoom(cardEl){'
        'return new Promise(function(resolve){'
            'if(!cardEl||BH_prefersReducedMotion||!BH_supportsTransition()){resolve();return;}'
            'var ov=document.getElementById("BH_overlay_card");'
            'if(!ov){resolve();return;}'
            'ov.innerHTML="";'
            'var clone=cardEl.cloneNode(true);'
            'clone.style.cssText="";'
            'clone.style.width=cardEl.offsetWidth+"px";'
            'clone.style.height=cardEl.offsetHeight+"px";'
            'clone.style.position="relative";'
            'var cid=cardEl.getAttribute("data-id");'
            'var cardData=cid&&window.BH_DECK_DATA?BH_DECK_DATA.find(function(c){return c.id===cid;}):null;'
            'if(cardData&&cardData.type==="gwang"){'
                'var lbl=document.createElement("div");'
                'lbl.textContent="[광] 20점";'
                'lbl.style.cssText="position:absolute;top:2px;left:0;right:0;text-align:center;font-size:18px;font-weight:900;color:#B8860B;background:rgba(255,215,0,0.85);border-radius:4px 4px 0 0;padding:1px 0;z-index:1;";'
                'clone.appendChild(lbl);'
            '}'
            'ov.appendChild(clone);'
            'ov.style.display="";'
            'ov.className="BH_overlay_card BH_anim_base";'
            'BH_playReveal();'
            'var spd=BH_getAnimSpd();'
            'requestAnimationFrame(function(){'
                'ov.classList.add("BH_anim_zoom");'
                'setTimeout(resolve,spd.zoom+spd.pause);'
            '});'
        '});'
    '}'
    # BH_animOverlap
    'function BH_animOverlap(playerCard,fieldCard){'
        'return new Promise(function(resolve){'
            'if(!playerCard||BH_prefersReducedMotion||!BH_supportsTransition()){resolve();return;}'
            'var spd=BH_getAnimSpd();'
            'playerCard.style.transition="transform "+spd.overlap+"ms ease-out";'
            'playerCard.style.transform="scale(1.1) translate(30px,-30px)";'
            'setTimeout(resolve,spd.overlap);'
        '});'
    '}'
    # BH_animMoveToCapture
    'function BH_animMoveToCapture(cardEl,targetPileEl){'
        'return new Promise(function(resolve){'
            'if(!cardEl||BH_prefersReducedMotion||!BH_supportsTransition()){'
                'var ov2=document.getElementById("BH_overlay_card");'
                'if(ov2){ov2.style.display="none";ov2.className="BH_overlay_card";ov2.innerHTML="";}resolve();return;'
            '}'
            'BH_playCapture();'
            'var spd=BH_getAnimSpd();'
            'cardEl.style.transition="transform "+spd.capture+"ms ease-in,opacity "+spd.capture+"ms ease-in";'
            'cardEl.style.transform="scale(0.8) translate(30px,-30px)";'
            'cardEl.style.opacity="0.5";'
            'setTimeout(function(){'
                'var ov=document.getElementById("BH_overlay_card");'
                'if(ov){ov.style.display="none";ov.className="BH_overlay_card";ov.innerHTML="";}resolve();'
            '},spd.capture);'
        '});'
    '}'
    # BH_wrapWithAnim
    'function BH_wrapWithAnim(originalFn){'
        'return function(cardEl,matchEl,captureEl){'
            'BH_GS.phase="ANIMATING";'
            'BH_animZoom(cardEl)'
            '.then(function(){'
                'var ov=document.getElementById("BH_overlay_card");'
                'var ovChild=ov&&ov.firstChild;'
                'return matchEl?BH_animOverlap(ovChild||cardEl,matchEl):Promise.resolve();'
            '})'
            '.then(function(){'
                'var ov=document.getElementById("BH_overlay_card");'
                'var ovChild=ov&&ov.firstChild;'
                'return captureEl?BH_animMoveToCapture(ovChild||cardEl,captureEl):('
                    '(function(){var ov2=document.getElementById("BH_overlay_card");if(ov2){ov2.style.display="none";ov2.className="BH_overlay_card";ov2.innerHTML="";}})(),'
                    'Promise.resolve()'
                ');'
            '})'
            '.then(function(){originalFn();})'
            '.catch(function(){BH_GS.phase="PLAYER_TURN";});'
        '};'
    '}'
)

insert_anim_before = 'function BH_initGame'
assert insert_anim_before in new_js_line, 'BH_initGame not found'
new_js_line = new_js_line.replace(insert_anim_before, anim_functions + insert_anim_before, 1)
print('Anim STEP4 OK. JS delta:', len(new_js_line) - len(old_js_line))

# ============================================================
# STEP 5: 호출 지점 교체
# ============================================================

# 5-A: BH_onFloorCardClick — BH_captureCards+setTimeout(BH_flipFromDeck_player,700) → BH_wrapWithAnim
old_floor = (
    'BH_playCardMatch();BH_captureCards(BH_GS.selectedCard,floorCard,\'player\');'
    'BH_GS.selectedCard=null;BH_renderBoard();BH_showFeedback(\'ok\');'
    'setTimeout(BH_flipFromDeck_player,700);'
)
new_floor = (
    'BH_playCardMatch();'
    'var _sel=BH_GS.selectedCard;'
    'var _selEl=document.querySelector(\'[data-id="\'+_sel.id+\'"]\');'
    'var _floorEl=document.querySelector(\'[data-id="\'+floorCard.id+\'"]\');'
    'var _pCap=document.querySelector(\'.BH_player_capture\');'
    'var _animFn=BH_wrapWithAnim(function(){'
        'BH_captureCards(_sel,floorCard,\'player\');'
        'BH_GS.selectedCard=null;'
        'BH_renderBoard();'
        'BH_showFeedback(\'ok\');'
        'BH_flipFromDeck_player();'
    '});'
    '_animFn(_selEl,_floorEl,_pCap);'
)

if old_floor in new_js_line:
    new_js_line = new_js_line.replace(old_floor, new_floor, 1)
    print('Floor STEP5-A OK')
else:
    # 다른 따옴표 형식 시도
    old_floor2 = (
        "BH_playCardMatch();BH_captureCards(BH_GS.selectedCard,floorCard,'player');"
        "BH_GS.selectedCard=null;BH_renderBoard();BH_showFeedback('ok');"
        "setTimeout(BH_flipFromDeck_player,700);"
    )
    if old_floor2 in new_js_line:
        new_floor2 = (
            "BH_playCardMatch();"
            "var _sel=BH_GS.selectedCard;"
            "var _selEl=document.querySelector('[data-id=\"'+_sel.id+'\"');"
            "var _floorEl=document.querySelector('[data-id=\"'+floorCard.id+'\"');"
            "var _pCap=document.querySelector('.BH_player_capture');"
            "var _animFn=BH_wrapWithAnim(function(){"
            "BH_captureCards(_sel,floorCard,'player');"
            "BH_GS.selectedCard=null;"
            "BH_renderBoard();"
            "BH_showFeedback('ok');"
            "BH_flipFromDeck_player();"
            "});"
            "_animFn(_selEl,_floorEl,_pCap);"
        )
        new_js_line = new_js_line.replace(old_floor2, new_floor2, 1)
        print('Floor STEP5-A OK (quote variant 2)')
    else:
        # 직접 문자열 검색으로 정확한 형식 확인
        idx = new_js_line.find('BH_captureCards(BH_GS.selectedCard,floorCard,')
        print('FLOOR CAPTURE POS:', idx)
        print('Context:', new_js_line[idx:idx+200])

print('STEP5 complete. Current JS length:', len(new_js_line))

# ============================================================
# STEP 5-B: BH_flipFromDeck_player 교체
# 기존: BH_captureCards(dc,matches[0],'player');BH_playCardMatch();...BH_renderBoard();setTimeout(BH_finishPlayerTurn,700);
# 변경: BH_wrapWithAnim 으로 래핑
# ============================================================
old_flip = (
    "function BH_flipFromDeck_player(){"
    "if(BH_GS.deck.length===0){BH_finishPlayerTurn();return;}"
    "var dc=BH_GS.deck.shift();"
    "BH_playCardFlip();"
    "BH_GS.deckFlipped=dc;"
    "var matches=BH_GS.floor.filter(function(c){return c.month===dc.month;});"
    "if(matches.length>0){BH_captureCards(dc,matches[0],'player');BH_playCardMatch();"
    "}else{BH_GS.floor.push(dc);BH_playCardPlace();}"
    "BH_renderBoard();setTimeout(BH_finishPlayerTurn,700);}"
)
new_flip = (
    "function BH_flipFromDeck_player(){"
    "if(BH_GS.deck.length===0){BH_finishPlayerTurn();return;}"
    "var dc=BH_GS.deck.shift();"
    "BH_playCardFlip();"
    "BH_GS.deckFlipped=dc;"
    "var matches=BH_GS.floor.filter(function(c){return c.month===dc.month;});"
    "if(matches.length>0){"
        "var _dcCopy=dc;var _m0Copy=matches[0];"
        "var _dcEl=null;"
        "var _m0El=document.querySelector('[data-id=\"'+_m0Copy.id+'\"');"
        "var _pCap2=document.querySelector('.BH_player_capture');"
        "var _animFn2=BH_wrapWithAnim(function(){"
            "BH_captureCards(_dcCopy,_m0Copy,'player');"
            "BH_playCardMatch();"
            "BH_renderBoard();"
            "BH_finishPlayerTurn();"
        "});"
        "_animFn2(_dcEl,_m0El,_pCap2);"
    "}else{"
        "BH_GS.floor.push(dc);"
        "BH_playCardPlace();"
        "BH_renderBoard();"
        "BH_finishPlayerTurn();"
    "}}"
)

if old_flip in new_js_line:
    new_js_line = new_js_line.replace(old_flip, new_flip, 1)
    print('Flip STEP5-B OK')
else:
    idx = new_js_line.find('function BH_flipFromDeck_player')
    print('FLIP EXACT SEARCH FAIL. Raw:', new_js_line[idx:idx+300])

# ============================================================
# STEP 5-C: BH_doAITurn 교체
# AI 턴에도 애니메이션 적용 (간소화: 매치 있을 때만 overlap 표시)
# ============================================================
old_ai = (
    "function BH_doAITurn(){"
    "if(BH_GS.aiHand.length===0){"
    "if(BH_checkGameOver()){BH_showResults();}else{BH_setPhase('PLAYER_TURN');BH_renderBoard();}return;}"
    "var card=BH_aiSelectCard();"
    "BH_playOpponentCard();"
    "var matches=BH_GS.floor.filter(function(c){return c.month===card.month;});"
    "if(matches.length>0){var target=matches[0];BH_captureCards(card,target,'ai');BH_renderBoard();"
    "}else{BH_GS.floor.push(card);BH_GS.aiHand=BH_GS.aiHand.filter(function(c){return c.id!==card.id;});BH_renderBoard();}"
    "setTimeout(function(){BH_flipFromDeck_ai(function(){if(BH_checkGameOver()){BH_showResults();}else{BH_setPhase('PLAYER_TURN');BH_renderBoard();}});},600);}"
)
new_ai = (
    "function BH_doAITurn(){"
    "if(BH_GS.aiHand.length===0){"
    "if(BH_checkGameOver()){BH_showResults();}else{BH_setPhase('PLAYER_TURN');BH_renderBoard();}return;}"
    "var card=BH_aiSelectCard();"
    "BH_playOpponentCard();"
    "var matches=BH_GS.floor.filter(function(c){return c.month===card.month;});"
    "if(matches.length>0){"
        "var target=matches[0];"
        "var _aiCardEl=null;"
        "var _aiFloorEl=document.querySelector('[data-id=\"'+target.id+'\"');"
        "var _aiCapEl=document.querySelector('.BH_ai_capture');"
        "var _aiAnimFn=BH_wrapWithAnim(function(){"
            "BH_captureCards(card,target,'ai');"
            "BH_renderBoard();"
            "setTimeout(function(){BH_flipFromDeck_ai(function(){"
                "if(BH_checkGameOver()){BH_showResults();}else{BH_setPhase('PLAYER_TURN');BH_renderBoard();}"
            "});},300);"
        "});"
        "_aiAnimFn(_aiCardEl,_aiFloorEl,_aiCapEl);"
    "}else{"
        "BH_GS.floor.push(card);"
        "BH_GS.aiHand=BH_GS.aiHand.filter(function(c){return c.id!==card.id;});"
        "BH_renderBoard();"
        "setTimeout(function(){BH_flipFromDeck_ai(function(){"
            "if(BH_checkGameOver()){BH_showResults();}else{BH_setPhase('PLAYER_TURN');BH_renderBoard();}"
        "});},600);"
    "}}"
)

if old_ai in new_js_line:
    new_js_line = new_js_line.replace(old_ai, new_ai, 1)
    print('AI STEP5-C OK')
else:
    idx = new_js_line.find('function BH_doAITurn')
    print('AI EXACT SEARCH FAIL. Raw:', new_js_line[idx:idx+300])

print('After 5-C. JS length:', len(new_js_line))

# ============================================================
# STEP 5-D: BH_noMatchPlayerCard setTimeout(BH_flipFromDeck_player,700) 제거
# 카드 매칭 없을 때 바닥에 놓는 경로 — 애니메이션 없이 직접 호출
# ============================================================
old_nomatch = (
    "BH_GS.phase='PLAYER_TURN';BH_showFeedback('ng');BH_renderBoard();"
    "setTimeout(BH_flipFromDeck_player,700);}"
)
new_nomatch = (
    "BH_GS.phase='PLAYER_TURN';BH_showFeedback('ng');BH_renderBoard();"
    "BH_flipFromDeck_player();}"
)

if old_nomatch in new_js_line:
    new_js_line = new_js_line.replace(old_nomatch, new_nomatch, 1)
    print('NoMatch STEP5-D OK')
else:
    idx = new_js_line.find('BH_noMatchPlayerCard')
    if idx >= 0:
        print('NoMatch STEP5-D FAIL. Context:', new_js_line[idx:idx+300])
    else:
        print('NoMatch STEP5-D FAIL. BH_noMatchPlayerCard not found')

print('After 5-D. JS length:', len(new_js_line))

# ============================================================
# STEP 6: 최종 파일 조립 및 저장
# ============================================================
output_lines = html_lines + [new_css_line, new_js_line, '', lines[75]]
output_content = '\n'.join(output_lines)

print('Output line count:', len(output_lines))
print('Output file size:', len(output_content))
print('Newline count in CSS:', new_css_line.count('\n'))
print('Newline count in JS:', new_js_line.count('\n'))

# 이모지 검사 (JS 내)
import re as _re
emoji_pattern = _re.compile(
    u'[\U00010000-\U0010ffff]', flags=_re.UNICODE
)
emoji_found = emoji_pattern.findall(new_js_line)
print('Emoji in JS:', len(emoji_found), '(should be 0)')
if emoji_found:
    print('Emoji samples:', emoji_found[:5])

# BH_ prefix 검증 (4개 함수 존재 확인)
for fn in ['function BH_animZoom', 'function BH_animOverlap', 'function BH_animMoveToCapture', 'function BH_wrapWithAnim',
           'function BH_playReveal', 'function BH_playCapture',
           'var BH_prefersReducedMotion', 'var BH_ANIM_SPEED']:
    print(fn + ':', fn in new_js_line)

with open('C:/Claude_code/widgets/post7_widget.html', 'w', encoding='utf-8') as f:
    f.write(output_content)
print('FILE SAVED OK')

