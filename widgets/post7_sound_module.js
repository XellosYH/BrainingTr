/* ===== post7_sound_module.js ===== */
/* sound 에이전트 v1.5 / brain_health_1.0 / Post #7 민화투 / 2026-05-23 */
/* 기존 BH_playCardPlace / BH_playCardMatch 대체 + BH_playCardFlip / BH_playOpponentCard 신규 */

/* ──────────────────────────────────────────────────────────────────
   READABLE 버전 (개발 참고용 — WP 직접 저장 금지)
   ────────────────────────────────────────────────────────────────── */

// 공통 의존성 (위젯에 이미 존재):
//   window.BH_SoundMuted   Boolean — 뮤트 상태
//   BH_getAC()             AudioContext 싱글톤 반환

// ─── 1. BH_playCardPlace() ──────────────────────────────────────────
// 손패 → 바닥 카드 내려놓기 ('탁' 둔탁음)
// Layer1: 화이트노이즈 버스트 0.12s (카드 표면 마찰)
// Layer2: 사인파 160→60Hz 하강 (충격감 서브베이스)
// vol: 0.35
function BH_playCardPlace() {
  if (window.BH_SoundMuted) return;
  try {
    var ac = BH_getAC(); var now = ac.currentTime;
    var bufLen = Math.floor(ac.sampleRate * 0.12);
    var buf = ac.createBuffer(1, bufLen, ac.sampleRate);
    var data = buf.getChannelData(0);
    for (var i = 0; i < bufLen; i++) {
      data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / bufLen, 1.8);
    }
    var src = ac.createBufferSource(); src.buffer = buf;
    var ng = ac.createGain();
    src.connect(ng); ng.connect(ac.destination);
    ng.gain.setValueAtTime(0.35, now);
    ng.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
    src.start(now);
    var osc = ac.createOscillator(); var og = ac.createGain();
    osc.connect(og); og.connect(ac.destination);
    osc.type = 'sine';
    osc.frequency.setValueAtTime(160, now);
    osc.frequency.exponentialRampToValueAtTime(60, now + 0.08);
    og.gain.setValueAtTime(0.4, now);
    og.gain.exponentialRampToValueAtTime(0.001, now + 0.1);
    osc.start(now); osc.stop(now + 0.12);
  } catch(e) {}
}

// ─── 2. BH_playCardFlip() ──────────────────────────────────────────
// 덱에서 패를 뒤집을 때 ('착' 날카로운 슬라이드음)
// Layer1: 고주파 노이즈 0.08s (카드 끝 긁힘)
// Layer2: sawtooth 800→200Hz 하강 (카드 뒤집히는 피치)
// vol: 0.18
function BH_playCardFlip() {
  if (window.BH_SoundMuted) return;
  try {
    var ac = BH_getAC(); var now = ac.currentTime;
    var bufLen = Math.floor(ac.sampleRate * 0.08);
    var buf = ac.createBuffer(1, bufLen, ac.sampleRate);
    var data = buf.getChannelData(0);
    for (var i = 0; i < bufLen; i++) {
      data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / bufLen, 2.5);
    }
    var src = ac.createBufferSource(); src.buffer = buf;
    var ng = ac.createGain();
    src.connect(ng); ng.connect(ac.destination);
    ng.gain.setValueAtTime(0.18, now);
    ng.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
    src.start(now);
    var osc = ac.createOscillator(); var og = ac.createGain();
    osc.connect(og); og.connect(ac.destination);
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(800, now);
    osc.frequency.exponentialRampToValueAtTime(200, now + 0.15);
    og.gain.setValueAtTime(0.15, now);
    og.gain.exponentialRampToValueAtTime(0.001, now + 0.15);
    osc.start(now); osc.stop(now + 0.15);
  } catch(e) {}
}

// ─── 3. BH_playCardMatch() ─────────────────────────────────────────
// 두 패가 맞아 획득할 때 ('착착' 이중 충돌음)
// 2연타: 노이즈 버스트 0.07s + 트라이앵글 2음 (0·100ms 간격)
// 두 번째 타격 음정 높음(550Hz) — 획득 성공 느낌
function BH_playCardMatch() {
  if (window.BH_SoundMuted) return;
  try {
    var ac = BH_getAC(); var now = ac.currentTime;
    [0, 0.1].forEach(function(delay, idx) {
      var t = now + delay;
      var bufLen = Math.floor(ac.sampleRate * 0.07);
      var buf = ac.createBuffer(1, bufLen, ac.sampleRate);
      var data = buf.getChannelData(0);
      for (var i = 0; i < bufLen; i++) {
        data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / bufLen, 2.0);
      }
      var src = ac.createBufferSource(); src.buffer = buf;
      var ng = ac.createGain();
      src.connect(ng); ng.connect(ac.destination);
      ng.gain.setValueAtTime(idx === 0 ? 0.3 : 0.35, t);
      ng.gain.exponentialRampToValueAtTime(0.001, t + 0.07);
      src.start(t);
      var osc = ac.createOscillator(); var og = ac.createGain();
      osc.connect(og); og.connect(ac.destination);
      osc.type = 'triangle';
      osc.frequency.value = idx === 0 ? 440 : 550;
      og.gain.setValueAtTime(0.2, t);
      og.gain.exponentialRampToValueAtTime(0.001, t + 0.18);
      osc.start(t); osc.stop(t + 0.18);
    });
  } catch(e) {}
}

// ─── 4. BH_playOpponentCard() ──────────────────────────────────────
// 상대(AI) 패 내기 — 플레이어와 다른 톤 (높고, 볼륨 작게)
// 서브베이스 240→100Hz (플레이어 160→60보다 높음 = 거리감)
// vol: 0.22 (플레이어 0.35보다 작음)
function BH_playOpponentCard() {
  if (window.BH_SoundMuted) return;
  try {
    var ac = BH_getAC(); var now = ac.currentTime;
    var bufLen = Math.floor(ac.sampleRate * 0.08);
    var buf = ac.createBuffer(1, bufLen, ac.sampleRate);
    var data = buf.getChannelData(0);
    for (var i = 0; i < bufLen; i++) {
      data[i] = (Math.random() * 2 - 1) * Math.pow(1 - i / bufLen, 2.2);
    }
    var src = ac.createBufferSource(); src.buffer = buf;
    var ng = ac.createGain();
    src.connect(ng); ng.connect(ac.destination);
    ng.gain.setValueAtTime(0.22, now);
    ng.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
    src.start(now);
    var osc = ac.createOscillator(); var og = ac.createGain();
    osc.connect(og); og.connect(ac.destination);
    osc.type = 'sine';
    osc.frequency.setValueAtTime(240, now);
    osc.frequency.exponentialRampToValueAtTime(100, now + 0.08);
    og.gain.setValueAtTime(0.25, now);
    og.gain.exponentialRampToValueAtTime(0.001, now + 0.10);
    osc.start(now); osc.stop(now + 0.10);
  } catch(e) {}
}

/* ──────────────────────────────────────────────────────────────────
   MINIFY 납품 블록 (game 에이전트 전달용 / WP <script> 태그 내 삽입)
   단일 행 — wpautop, wp_staticize_emoji 방어 완료
   ────────────────────────────────────────────────────────────────── */

function BH_playCardPlace(){if (window.BH_SoundMuted) return;try{var ac=BH_getAC();var now=ac.currentTime;var bufLen=Math.floor(ac.sampleRate*0.12);var buf=ac.createBuffer(1,bufLen,ac.sampleRate);var data=buf.getChannelData(0);for (var i=0;i<bufLen;i++){data[i]=(Math.random()*2-1)*Math.pow(1-i/bufLen,1.8);}var src=ac.createBufferSource();src.buffer=buf;var ng=ac.createGain();src.connect(ng);ng.connect(ac.destination);ng.gain.setValueAtTime(0.35,now);ng.gain.exponentialRampToValueAtTime(0.001,now+0.12);src.start(now);var osc=ac.createOscillator();var og=ac.createGain();osc.connect(og);og.connect(ac.destination);osc.type='sine';osc.frequency.setValueAtTime(160,now);osc.frequency.exponentialRampToValueAtTime(60,now+0.08);og.gain.setValueAtTime(0.4,now);og.gain.exponentialRampToValueAtTime(0.001,now+0.1);osc.start(now);osc.stop(now+0.12);}catch(e){}}function BH_playCardFlip(){if (window.BH_SoundMuted) return;try{var ac=BH_getAC();var now=ac.currentTime;var bufLen=Math.floor(ac.sampleRate*0.08);var buf=ac.createBuffer(1,bufLen,ac.sampleRate);var data=buf.getChannelData(0);for (var i=0;i<bufLen;i++){data[i]=(Math.random()*2-1)*Math.pow(1-i/bufLen,2.5);}var src=ac.createBufferSource();src.buffer=buf;var ng=ac.createGain();src.connect(ng);ng.connect(ac.destination);ng.gain.setValueAtTime(0.18,now);ng.gain.exponentialRampToValueAtTime(0.001,now+0.08);src.start(now);var osc=ac.createOscillator();var og=ac.createGain();osc.connect(og);og.connect(ac.destination);osc.type='sawtooth';osc.frequency.setValueAtTime(800,now);osc.frequency.exponentialRampToValueAtTime(200,now+0.15);og.gain.setValueAtTime(0.15,now);og.gain.exponentialRampToValueAtTime(0.001,now+0.15);osc.start(now);osc.stop(now+0.15);}catch(e){}}function BH_playCardMatch(){if (window.BH_SoundMuted) return;try{var ac=BH_getAC();var now=ac.currentTime;[0,0.1].forEach(function(delay,idx){var t=now+delay;var bufLen=Math.floor(ac.sampleRate*0.07);var buf=ac.createBuffer(1,bufLen,ac.sampleRate);var data=buf.getChannelData(0);for (var i=0;i<bufLen;i++){data[i]=(Math.random()*2-1)*Math.pow(1-i/bufLen,2.0);}var src=ac.createBufferSource();src.buffer=buf;var ng=ac.createGain();src.connect(ng);ng.connect(ac.destination);ng.gain.setValueAtTime(idx===0 ? 0.3 : 0.35,t);ng.gain.exponentialRampToValueAtTime(0.001,t+0.07);src.start(t);var osc=ac.createOscillator();var og=ac.createGain();osc.connect(og);og.connect(ac.destination);osc.type='triangle';osc.frequency.value=idx===0 ? 440 : 550;og.gain.setValueAtTime(0.2,t);og.gain.exponentialRampToValueAtTime(0.001,t+0.18);osc.start(t);osc.stop(t+0.18);});}catch(e){}}function BH_playOpponentCard(){if (window.BH_SoundMuted) return;try{var ac=BH_getAC();var now=ac.currentTime;var bufLen=Math.floor(ac.sampleRate*0.08);var buf=ac.createBuffer(1,bufLen,ac.sampleRate);var data=buf.getChannelData(0);for (var i=0;i<bufLen;i++){data[i]=(Math.random()*2-1)*Math.pow(1-i/bufLen,2.2);}var src=ac.createBufferSource();src.buffer=buf;var ng=ac.createGain();src.connect(ng);ng.connect(ac.destination);ng.gain.setValueAtTime(0.22,now);ng.gain.exponentialRampToValueAtTime(0.001,now+0.08);src.start(now);var osc=ac.createOscillator();var og=ac.createGain();osc.connect(og);og.connect(ac.destination);osc.type='sine';osc.frequency.setValueAtTime(240,now);osc.frequency.exponentialRampToValueAtTime(100,now+0.08);og.gain.setValueAtTime(0.25,now);og.gain.exponentialRampToValueAtTime(0.001,now+0.10);osc.start(now);osc.stop(now+0.10);}catch(e){}}

/* ──────────────────────────────────────────────────────────────────
   game 에이전트 통합 가이드
   ────────────────────────────────────────────────────────────────── */

/* [통합 방법]
 *
 * 1. 위 MINIFY 블록을 post7_widget_v2.html의 <script> 태그 내
 *    기존 BH_playCardPlace 함수 정의 앞에 삽입
 *    (기존 BH_playCardPlace, BH_playCardMatch 함수는 제거)
 *
 * 2. 트리거 위치별 함수 호출 교체:
 *
 *    [기존 → 신규]
 *    BH_playCardPlace()   →  그대로 사용 (업그레이드 버전으로 대체)
 *    BH_playCardMatch()   →  그대로 사용 (업그레이드 버전으로 대체)
 *
 *    [신규 추가]
 *    BH_flipFromDeck_player() 안: BH_playCardFlip() 추가
 *    BH_flipFromDeck_ai() 안:    BH_playCardFlip() 추가
 *    BH_doAITurn() 안 카드 내기: BH_playOpponentCard() 추가
 *
 * 3. 구체적 삽입 위치 (post7_widget_v2.html 기준):
 *
 *    function BH_flipFromDeck_player() {
 *      ...
 *      var dc = BH_GS.deck.shift();
 *      BH_playCardFlip();  // ← 이 줄 추가 (덱 뒤집기 직후)
 *      ...
 *    }
 *
 *    function BH_flipFromDeck_ai(cb) {
 *      ...
 *      var dc = BH_GS.deck.shift();
 *      BH_playCardFlip();  // ← 이 줄 추가
 *      ...
 *    }
 *
 *    function BH_doAITurn() {
 *      ...
 *      var card = BH_aiSelectCard();
 *      BH_playOpponentCard();  // ← 이 줄 추가 (AI 카드 선택 직후)
 *      ...
 *    }
 *
 * 4. 효과음 매핑 전체 (통합 후):
 *
 *    이벤트                     함수                  출처
 *    ──────────────────────────────────────────────────────
 *    버튼 클릭                  BH_playClick()        기존 유지
 *    손패 카드 선택             BH_playClick()        기존 유지
 *    손패 → 바닥 내려놓기      BH_playCardPlace()    v1.2 교체
 *    덱 카드 뒤집기             BH_playCardFlip()     v1.2 신규
 *    짝 맞추기 성공             BH_playCardMatch()    v1.2 교체
 *    AI 카드 내기               BH_playOpponentCard() v1.2 신규
 *    족보 달성                  BH_playJokboSound()   기존 유지
 *    게임 승리 결과             BH_playFanfare()      기존 유지
 *    게임 패배 결과             BH_playWrong()        기존 유지
 *    새 게임 시작               BH_playReset()        기존 유지
 *
 * 5. 제거 대상 (기존 위젯에서 삭제):
 *    window.BH_playCardPlace = function(){...}  (기존 단순 버전)
 *    window.BH_playCardMatch = function(){...}  (기존 단순 버전)
 *
 * 6. WP 업로드 시 주의:
 *    - MINIFY 블록만 추출하여 위젯 <script> 에 삽입
 *    - 개행 포함 readable 버전 직접 WP 저장 금지 (wpautop 파괴)
 */
