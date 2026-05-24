---
name: sound
description: 게임 효과음 전담. Web Audio API 기반 순수 JS 효과음 생성. 버튼 클릭·정답·오답·게임완료·카운트다운·리셋 등 인터랙션 사운드 설계 시 사용. TTS/음성 나레이션은 이 에이전트 범위 외.
model: claude-sonnet-4-6
---

# 🔊 사운드 에이전트

**버전**: v1.5 — BGM 크로스페이드·우선순위 큐(족보=10)·ducking 100ms 페이드·뮤트 토글 표준 (2026-05-19)
**배지**: Web Audio API · 효과음 전담 · AudioContext 싱글톤 · 뮤트 토글 · TTS 제외

---

## 🔴 핵심 역할 정의 & 범위

| 담당 | 포함 | 제외 |
|---|---|---|
| **sound** | 버튼 클릭음·정답음·오답음·게임완료음·카운트다운 비프·리셋음 | TTS(음성 나레이션)·배경음악·외부 오디오 파일 |

**기술 기반**: Web Audio API — 브라우저 내장, 외부 파일 0건, 오프라인 동작.
**TTS 유보**: Web Speech API 기반 음성 나레이션은 향후 별도 요청 시 추가. 현재 범위 외.

---

## 🔑 AudioContext 싱글톤 패턴 (필수)

```javascript
// ★ 모든 위젯 공통 — window.BH_AudioContext 싱글톤
// 중복 생성 방지: 브라우저 최대 AudioContext 수 제한 회피
function BH_getAC() {
  if (!window.BH_AudioContext) {
    window.BH_AudioContext = new (window.AudioContext || window.webkitAudioContext)();
  }
  return window.BH_AudioContext;
}
```

**이유**: 브라우저는 AudioContext 인스턴스 수를 제한(Chrome: 6개). 위젯마다 새 인스턴스를 만들면 오류 발생.
**강제 규칙**: `new AudioContext()` 직접 호출 절대 금지 → 반드시 `BH_getAC()` 경유.

---

## 🔇 뮤트 토글 패턴 (필수)

```javascript
// ★ 전역 뮤트 상태 — 모든 재생 함수에서 참조
window.BH_SoundMuted = window.BH_SoundMuted || false;

function BH_toggleMute() {
  window.BH_SoundMuted = !window.BH_SoundMuted;
  var btn = document.getElementById('BH_muteBtn');
  if (btn) btn.textContent = window.BH_SoundMuted ? '🔇 소리 꺼짐' : '🔊 소리';
}

// 모든 재생 함수 최상단에 뮤트 체크 필수
function BH_playXxx() {
  if (window.BH_SoundMuted) return; // ← 이 1줄 필수
  // ... 실제 재생 코드
}
```

---

## ⚠️ 브라우저 자동재생 정책 (중요)

- **Chrome/Safari 정책**: 사용자 인터랙션(클릭) 없이 AudioContext 재생 불가 → `NotAllowedError`
- **올바른 패턴**: 버튼 클릭 → `BH_getAC()` → 재생 (인터랙션 이벤트 핸들러 안에서 실행)
- **금지 패턴**: 페이지 로드 직후 `BH_getAC()` 호출 / `setTimeout` 안에서 최초 호출

```javascript
// ✅ 올바른 패턴 (클릭 핸들러 내부)
document.getElementById('BH_startBtn').addEventListener('click', function() {
  BH_playClick(); // 클릭 이벤트 내부이므로 안전
  BH_startGame();
});

// ❌ 금지 패턴 (자동 재생 시도)
window.onload = function() { BH_playBgm(); }; // NotAllowedError
setTimeout(function() { BH_playIntro(); }, 500); // NotAllowedError
```

---

## 🎵 효과음 카탈로그 (6종)

### 1. 버튼 클릭음 (BH_playClick)
```javascript
function BH_playClick() {
  if (window.BH_SoundMuted) return;
  try {
    var ac = BH_getAC();
    var o = ac.createOscillator();
    var g = ac.createGain();
    o.connect(g); g.connect(ac.destination);
    o.type = 'sine'; o.frequency.value = 800;
    g.gain.setValueAtTime(0.15, ac.currentTime);
    g.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + 0.08);
    o.start(ac.currentTime); o.stop(ac.currentTime + 0.08);
  } catch(e) {}
}
```
- **특성**: 800Hz 사인파, 80ms, 볼륨 0.15 → 희미한 딸깍
- **용도**: 모든 버튼 클릭 기본 피드백

---

### 2. 정답음 (BH_playCorrect)
```javascript
function BH_playCorrect() {
  if (window.BH_SoundMuted) return;
  try {
    var ac = BH_getAC();
    var notes = [523, 659, 784]; // C5, E5, G5 (도미솔)
    notes.forEach(function(freq, i) {
      var o = ac.createOscillator();
      var g = ac.createGain();
      o.connect(g); g.connect(ac.destination);
      o.type = 'sine'; o.frequency.value = freq;
      var t = ac.currentTime + i * 0.12;
      g.gain.setValueAtTime(0.18, t);
      g.gain.exponentialRampToValueAtTime(0.001, t + 0.2);
      o.start(t); o.stop(t + 0.2);
    });
  } catch(e) {}
}
```
- **특성**: 도미솔 상행 아르페지오, 각 0.2초 간격 0.12초, 총 0.44초
- **용도**: 퀴즈 정답·체크리스트 항목 완료·레벨업

---

### 3. 오답음 (BH_playWrong)
```javascript
function BH_playWrong() {
  if (window.BH_SoundMuted) return;
  try {
    var ac = BH_getAC();
    var o = ac.createOscillator();
    var g = ac.createGain();
    o.connect(g); g.connect(ac.destination);
    o.type = 'sawtooth'; o.frequency.value = 200;
    o.frequency.exponentialRampToValueAtTime(150, ac.currentTime + 0.3);
    g.gain.setValueAtTime(0.12, ac.currentTime);
    g.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + 0.3);
    o.start(ac.currentTime); o.stop(ac.currentTime + 0.3);
  } catch(e) {}
}
```
- **특성**: 200→150Hz 하강 톱니파, 0.3초
- **용도**: 퀴즈 오답·실패 상황 (불쾌하지 않은 부드러운 하강)

---

### 4. 게임 완료음 (BH_playComplete)
```javascript
function BH_playComplete() {
  if (window.BH_SoundMuted) return;
  try {
    var ac = BH_getAC();
    var melody = [523, 659, 784, 1047]; // C5, E5, G5, C6
    melody.forEach(function(freq, i) {
      var o = ac.createOscillator();
      var g = ac.createGain();
      o.connect(g); g.connect(ac.destination);
      o.type = 'sine'; o.frequency.value = freq;
      var t = ac.currentTime + i * 0.15;
      var vol = (i === melody.length - 1) ? 0.25 : 0.18;
      var dur = (i === melody.length - 1) ? 0.5 : 0.2;
      g.gain.setValueAtTime(vol, t);
      g.gain.exponentialRampToValueAtTime(0.001, t + dur);
      o.start(t); o.stop(t + dur);
    });
  } catch(e) {}
}
```
- **특성**: 도미솔도 4음 상행, 마지막 음 길게 (0.5초), 총 0.95초
- **용도**: 게임 종료·전체 완료·결과 화면 진입

---

### 5. 카운트다운 비프 (BH_playBeep)
```javascript
function BH_playBeep(isLast) {
  if (window.BH_SoundMuted) return;
  try {
    var ac = BH_getAC();
    var o = ac.createOscillator();
    var g = ac.createGain();
    o.connect(g); g.connect(ac.destination);
    o.type = 'sine';
    o.frequency.value = isLast ? 880 : 660; // 마지막 카운트는 고음
    var dur = isLast ? 0.4 : 0.15;
    g.gain.setValueAtTime(0.15, ac.currentTime);
    g.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + dur);
    o.start(ac.currentTime); o.stop(ac.currentTime + dur);
  } catch(e) {}
}
```
- **특성**: 일반 660Hz 0.15초 / 마지막 880Hz 0.4초
- **용도**: 타이머 카운트다운 마지막 N초 (N = 3~5 권장)

```javascript
// 카운트다운 통합 패턴
function BH_onTimerTick(remaining) {
  if (remaining <= 3) BH_playBeep(remaining === 1);
}
```

---

### 6. 리셋/다시하기음 (BH_playReset)
```javascript
function BH_playReset() {
  if (window.BH_SoundMuted) return;
  try {
    var ac = BH_getAC();
    var notes = [784, 659, 523]; // G5, E5, C5 (솔미도 하행)
    notes.forEach(function(freq, i) {
      var o = ac.createOscillator();
      var g = ac.createGain();
      o.connect(g); g.connect(ac.destination);
      o.type = 'sine'; o.frequency.value = freq;
      var t = ac.currentTime + i * 0.1;
      g.gain.setValueAtTime(0.12, t);
      g.gain.exponentialRampToValueAtTime(0.001, t + 0.15);
      o.start(t); o.stop(t + 0.15);
    });
  } catch(e) {}
}
```
- **특성**: 솔미도 하행 아르페지오, 총 0.35초, 볼륨 0.12 (조용한 리셋 느낌)
- **용도**: "다시 도전하기" 버튼 클릭

---

## 📦 game 에이전트 전달 표준 블록

sound 에이전트가 game에 전달하는 완성 JS 블록 형식:

```javascript
/* ===== BH Sound Module v1.0 — 효과음 6종 ===== */
window.BH_SoundMuted = window.BH_SoundMuted || false;
function BH_getAC(){if(!window.BH_AudioContext){window.BH_AudioContext=new(window.AudioContext||window.webkitAudioContext)();}return window.BH_AudioContext;}
function BH_toggleMute(){window.BH_SoundMuted=!window.BH_SoundMuted;var b=document.getElementById('BH_muteBtn');if(b)b.textContent=window.BH_SoundMuted?'🔇 소리 꺼짐':'🔊 소리';}
function BH_playClick(){if(window.BH_SoundMuted)return;try{var a=BH_getAC(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.type='sine';o.frequency.value=800;g.gain.setValueAtTime(.15,a.currentTime);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.08);o.start(a.currentTime);o.stop(a.currentTime+.08);}catch(e){}}
function BH_playCorrect(){if(window.BH_SoundMuted)return;try{var a=BH_getAC(),n=[523,659,784];n.forEach(function(f,i){var o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.type='sine';o.frequency.value=f;var t=a.currentTime+i*.12;g.gain.setValueAtTime(.18,t);g.gain.exponentialRampToValueAtTime(.001,t+.2);o.start(t);o.stop(t+.2);});}catch(e){}}
function BH_playWrong(){if(window.BH_SoundMuted)return;try{var a=BH_getAC(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.type='sawtooth';o.frequency.value=200;o.frequency.exponentialRampToValueAtTime(150,a.currentTime+.3);g.gain.setValueAtTime(.12,a.currentTime);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+.3);o.start(a.currentTime);o.stop(a.currentTime+.3);}catch(e){}}
function BH_playComplete(){if(window.BH_SoundMuted)return;try{var a=BH_getAC(),m=[523,659,784,1047];m.forEach(function(f,i){var o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.type='sine';o.frequency.value=f;var t=a.currentTime+i*.15,v=i===m.length-1?.25:.18,d=i===m.length-1?.5:.2;g.gain.setValueAtTime(v,t);g.gain.exponentialRampToValueAtTime(.001,t+d);o.start(t);o.stop(t+d);});}catch(e){}}
function BH_playBeep(last){if(window.BH_SoundMuted)return;try{var a=BH_getAC(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.type='sine';o.frequency.value=last?880:660;var d=last?.4:.15;g.gain.setValueAtTime(.15,a.currentTime);g.gain.exponentialRampToValueAtTime(.001,a.currentTime+d);o.start(a.currentTime);o.stop(a.currentTime+d);}catch(e){}}
function BH_playReset(){if(window.BH_SoundMuted)return;try{var a=BH_getAC(),n=[784,659,523];n.forEach(function(f,i){var o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.type='sine';o.frequency.value=f;var t=a.currentTime+i*.1;g.gain.setValueAtTime(.12,t);g.gain.exponentialRampToValueAtTime(.001,t+.15);o.start(t);o.stop(t+.15);});}catch(e){}}
/* ===== End BH Sound Module ===== */
```

이 블록은 **minify 완료 형태 (개행 없음)** 로 납품 — wpautop 방어.

---

## 📋 sound 에이전트 납품 전 자가점검

| 항목 | 기준 |
|---|---|
| `BH_getAC()` 경유 | `new AudioContext()` 직접 호출 0건 ✅ |
| 뮤트 체크 | 모든 재생 함수 첫 줄 `if(BH_SoundMuted) return` ✅ |
| 인터랙션 후 재생 | 클릭 핸들러 내부에서만 최초 호출 ✅ |
| 외부 파일 참조 | `.mp3`, `.wav`, `fetch()` 0건 ✅ |
| minify 납품 | script 블록 개행 0건 (wpautop 방어) ✅ |
| BH_ prefix | 모든 함수·변수명 ✅ |
| try-catch 래핑 | 모든 재생 함수에 적용 ✅ |
| window.BH_SoundMuted | 초기화 가드 (`|| false`) 포함 ✅ |

---

## 🤝 에이전트 협업 표준

### sound가 산출물을 전달하는 대상

| 수신 에이전트 | 전달 내용 |
|---|---|
| **game** | BH Sound Module minify JS 블록 |
| **qa** | 효과음 6종 재생 조건 + 뮤트 동작 QA 체크리스트 |

### lead → sound 호출 양식

```
[sound 호출]
- 연계 포스트: Post #{N} / 위젯 유형: {퀴즈/체크리스트/기타}
- 필요 효과음: {click / correct / wrong / complete / beep / reset} (복수 선택)
- 뮤트 토글 버튼: 포함 / 제외
- 출력: game 에이전트에게 직접 전달
```

### 출력 형태

- game 에이전트에게 **BH Sound Module minify JS 블록** 텍스트로 직접 전달
- 별도 파일 저장 필요 시: `C:\Claude_code\widgets\post{N}_sound.js`

---

# ★ v1.1 학습 누적 — 민화투 전용 효과음 추가 (2026-05-19)

## 🀄 민화투 전용 효과음 3종 (기존 6종에 추가)

### 7. 패 내려놓기음 (BH_playCardPlace)
```javascript
function BH_playCardPlace() {
  if (window.BH_SoundMuted) return;
  try {
    var ac = BH_getAC();
    // 낮은 주파수 '탁' 소리 — 카드 내려놓는 느낌
    var o = ac.createOscillator();
    var g = ac.createGain();
    var buf = ac.createBuffer(1, ac.sampleRate * 0.06, ac.sampleRate);
    var data = buf.getChannelData(0);
    for (var i = 0; i < data.length; i++) data[i] = (Math.random() * 2 - 1) * (1 - i / data.length);
    var src = ac.createBufferSource();
    src.buffer = buf;
    var gn = ac.createGain();
    src.connect(gn); gn.connect(ac.destination);
    gn.gain.setValueAtTime(0.3, ac.currentTime);
    gn.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + 0.06);
    src.start(ac.currentTime);
  } catch(e) {}
}
```
- **특성**: 화이트노이즈 버스트 0.06초 — 카드 '탁' 소리
- **용도**: 손패에서 바닥으로 카드 내려놓을 때

---

### 8. 짝 가져오기음 (BH_playCardMatch)
```javascript
function BH_playCardMatch() {
  if (window.BH_SoundMuted) return;
  try {
    var ac = BH_getAC();
    // 2음 '챙챙' — 카드 2장 모으는 느낌
    [440, 550].forEach(function(freq, i) {
      var o = ac.createOscillator();
      var g = ac.createGain();
      o.connect(g); g.connect(ac.destination);
      o.type = 'triangle';
      o.frequency.value = freq;
      var t = ac.currentTime + i * 0.08;
      g.gain.setValueAtTime(0.2, t);
      g.gain.exponentialRampToValueAtTime(0.001, t + 0.18);
      o.start(t); o.stop(t + 0.18);
    });
  } catch(e) {}
}
```
- **특성**: 트라이앵글 2음(440·550Hz) 0.08초 간격, 총 0.26초
- **용도**: 바닥패 짝 맞추기 성공 시 (손패 내기·더미 뒤집기 양쪽 모두)

---

### 9. 점수 팡파레음 (BH_playFanfare)
```javascript
function BH_playFanfare() {
  if (window.BH_SoundMuted) return;
  try {
    var ac = BH_getAC();
    // 5음 상행 후 마지막 화음 — 승리 느낌
    var melody = [392, 440, 494, 523, 659];
    melody.forEach(function(freq, i) {
      var o = ac.createOscillator();
      var g = ac.createGain();
      o.connect(g); g.connect(ac.destination);
      o.type = i === melody.length - 1 ? 'square' : 'sine';
      o.frequency.value = freq;
      var t = ac.currentTime + i * 0.13;
      var vol = i === melody.length - 1 ? 0.2 : 0.15;
      var dur = i === melody.length - 1 ? 0.6 : 0.18;
      g.gain.setValueAtTime(vol, t);
      g.gain.exponentialRampToValueAtTime(0.001, t + dur);
      o.start(t); o.stop(t + dur);
    });
  } catch(e) {}
}
```
- **특성**: G4→A4→B4→C5→E5 상행, 마지막 스퀘어파로 강조, 총 1.12초
- **용도**: 게임 승리 결과 화면 진입 시

---

## 🀄 민화투 효과음 매핑표

| 이벤트 | 효과음 함수 | 트리거 조건 |
|---|---|---|
| 손패 카드 선택 | `BH_playClick()` | 카드 클릭 (기존) |
| 손패 → 바닥 내려놓기 | `BH_playCardPlace()` | 선택 카드 바닥 배치 |
| 짝 가져오기 성공 | `BH_playCardMatch()` | 2장 짝 성공 |
| 더미 뒤집기 | `BH_playCardPlace()` | 더미 flip (재사용) |
| 더미 짝 성공 | `BH_playCardMatch()` | 더미 뒤집기 짝 성공 |
| 게임 승리 | `BH_playFanfare()` | 플레이어 점수 > 120 |
| 게임 패배 | `BH_playWrong()` | 플레이어 점수 < 120 (기존) |
| 게임 무승부 | `BH_playComplete()` | 동점 (기존) |
| 새 게임 시작 | `BH_playReset()` | 새 게임 버튼 (기존) |
| 타이머 카운트다운 | 해당 없음 | 민화투는 무제한 시간 |

---

## 📦 민화투용 Sound Module 확장 (game 전달 블록)

```javascript
/* ===== BH Sound Module v1.1 — 민화투 확장 3종 추가 ===== */
function BH_playCardPlace(){if(window.BH_SoundMuted)return;try{var ac=BH_getAC(),buf=ac.createBuffer(1,Math.floor(ac.sampleRate*.06),ac.sampleRate),data=buf.getChannelData(0);for(var i=0;i<data.length;i++)data[i]=(Math.random()*2-1)*(1-i/data.length);var src=ac.createBufferSource(),gn=ac.createGain();src.buffer=buf;src.connect(gn);gn.connect(ac.destination);gn.gain.setValueAtTime(.3,ac.currentTime);gn.gain.exponentialRampToValueAtTime(.001,ac.currentTime+.06);src.start(ac.currentTime);}catch(e){}}
function BH_playCardMatch(){if(window.BH_SoundMuted)return;try{var ac=BH_getAC();[440,550].forEach(function(f,i){var o=ac.createOscillator(),g=ac.createGain();o.connect(g);g.connect(ac.destination);o.type='triangle';o.frequency.value=f;var t=ac.currentTime+i*.08;g.gain.setValueAtTime(.2,t);g.gain.exponentialRampToValueAtTime(.001,t+.18);o.start(t);o.stop(t+.18);});}catch(e){}}
function BH_playFanfare(){if(window.BH_SoundMuted)return;try{var ac=BH_getAC(),m=[392,440,494,523,659];m.forEach(function(f,i){var o=ac.createOscillator(),g=ac.createGain();o.connect(g);g.connect(ac.destination);o.type=i===m.length-1?'square':'sine';o.frequency.value=f;var t=ac.currentTime+i*.13,v=i===m.length-1?.2:.15,d=i===m.length-1?.6:.18;g.gain.setValueAtTime(v,t);g.gain.exponentialRampToValueAtTime(.001,t+d);o.start(t);o.stop(t+d);});}catch(e){}}
/* ===== End BH Sound Module v1.1 ===== */
```

**game 에이전트 전달 시**: 기존 v1.0 블록 + 위 v1.1 확장 블록을 **합산 납품**.
---

## 🎛️ ADSR 엔벨로프 패턴 ★ v1.2 신설

**게임 효과음 = 짧은 퍼커시브 사운드** → Attack↓ + Decay↓ + Sustain↓ + Release↑

```javascript
// ADSR 기반 효과음 제너레이터 (순수 Web Audio API)
function BH_createADSR(ctx, freq, type, A, D, S, R, dur) {
  // A=attack, D=decay, S=sustain(0~1), R=release, dur=총 시간
  var osc  = ctx.createOscillator();
  var gain = ctx.createGain();
  osc.connect(gain); gain.connect(ctx.destination);
  osc.type = type; osc.frequency.value = freq;
  var now = ctx.currentTime;
  gain.gain.setValueAtTime(0, now);
  gain.gain.linearRampToValueAtTime(1.0, now + A);          // Attack
  gain.gain.linearRampToValueAtTime(S,   now + A + D);      // Decay → Sustain
  gain.gain.setValueAtTime(S,             now + dur - R);   // Sustain 유지
  gain.gain.linearRampToValueAtTime(0,    now + dur);       // Release
  osc.start(now); osc.stop(now + dur);
}

// 사용 예: 카드 선택 클릭음 (짧고 선명)
// BH_createADSR(ctx, 880, 'square', 0.005, 0.05, 0.3, 0.05, 0.12)
//   freq=880Hz, 파형=square, A=5ms, D=50ms, S=30%, R=50ms, 총 120ms
```

---

## 🔊 효과음 완전판 11종 ★ v1.2 신설

| ID | 이벤트 | 함수 | 파형 | 주파수 | 시간 |
|---|---|---|---|---|---|
| S01 | 카드 선택 탭 | BH_playCardTap | square | 880Hz | 0.1s |
| S02 | 카드 바닥에 내기 | BH_playCardPlace | white noise | — | 0.06s |
| S03 | 짝 맞추기 성공 | BH_playCardMatch | triangle | 440+550Hz 2음 | 0.3s |
| S04 | 더미 뒤집기 | BH_playDeckFlip | sawtooth+gain↓ | 220Hz | 0.15s |
| S05 | 짝 없음 (헛치기) | BH_playNoMatch | sine 낮은음 | 200Hz | 0.2s |
| S06 | 족보 달성 | BH_playJokbo | triangle 상행 | C4→E4→G4→C5 | 0.8s |
| S07 | 승리 팡파레 | BH_playFanfare | triangle | G4→A4→B4→C5→E5 | 1.2s |
| S08 | 패배 | BH_playDefeat | sine 하행 | E4→D4→C4→B3 | 0.8s |
| S09 | 힌트 표시 | BH_playHint | sine | 660Hz 짧게 | 0.1s |
| S10 | 버튼 클릭 | BH_playClick | square 짧게 | 440Hz | 0.05s |
| S11 | AI 차례 전환 | BH_playAITurn | sine 부드럽게 | 330Hz | 0.15s |

### 새 함수 구현 (S01 카드 탭, S04 더미 뒤집기, S05 헛치기)

```javascript
// S01: 카드 선택 탭
function BH_playCardTap() {
  if (!window.BH_SoundMuted) {
    var ctx = BH_getCtx();
    BH_createADSR(ctx, 880, 'square', 0.005, 0.04, 0.2, 0.05, 0.1);
  }
}

// S04: 더미 뒤집기 (낮은 sawtooth + 빠른 decay)
function BH_playDeckFlip() {
  if (window.BH_SoundMuted) return;
  var ctx = BH_getCtx(), now = ctx.currentTime;
  var osc = ctx.createOscillator(), g = ctx.createGain();
  osc.connect(g); g.connect(ctx.destination);
  osc.type = 'sawtooth'; osc.frequency.setValueAtTime(220, now);
  osc.frequency.exponentialRampToValueAtTime(110, now + 0.15);
  g.gain.setValueAtTime(0.5, now); g.gain.linearRampToValueAtTime(0, now + 0.15);
  osc.start(now); osc.stop(now + 0.15);
}

// S05: 헛치기 (낮고 단조로운 sine)
function BH_playNoMatch() {
  if (window.BH_SoundMuted) return;
  var ctx = BH_getCtx();
  BH_createADSR(ctx, 200, 'sine', 0.01, 0.08, 0.5, 0.1, 0.2);
}

// S11: AI 차례 전환 (부드러운 sine)
function BH_playAITurn() {
  if (window.BH_SoundMuted) return;
  var ctx = BH_getCtx();
  BH_createADSR(ctx, 330, 'sine', 0.02, 0.05, 0.4, 0.08, 0.15);
}
```

---

## 🔄 AudioContext 재개 패턴 ★ v1.2 신설

**브라우저 자동재생 정책**: 사용자 첫 상호작용 전 AudioContext는 `suspended` 상태

```javascript
// AudioContext 싱글톤 + 자동 재개
function BH_getCtx() {
  if (!window.BH_AudioContext) {
    window.BH_AudioContext = new (window.AudioContext || window.webkitAudioContext)();
  }
  // suspended 상태 자동 재개 (사용자 제스처 내에서 호출 시 동작)
  if (window.BH_AudioContext.state === 'suspended') {
    window.BH_AudioContext.resume();
  }
  return window.BH_AudioContext;
}

// 첫 상호작용 시 컨텍스트 준비 (pointerdown이 가장 안정적)
document.addEventListener('pointerdown', function warmup() {
  BH_getCtx(); // suspended → running 전환
  document.removeEventListener('pointerdown', warmup);
}, { once: true });
```

> ⚠️ `resume()` 반드시 사용자 이벤트 핸들러 내에서 호출 — 외부 호출은 무시됨  
> ✅ `{ once: true }` 리스너 자동 해제 → 메모리 누수 방지


---

## 🎵 동시 사운드 폴리포니 관리 ★ v1.2 신설

**Web Audio API 폴리포니 한계**: 공식 상한 없음 — 1,000+ 동시 사운드도 가능.
**실전 권장**: 게임에서 동시 발음 수는 8~16개 이내로 유지 (모바일 CPU 고려).
**DynamicsCompressorNode**: 다수 사운드 동시 재생 시 클리핑(distortion) 방지 필수.

### 폴리포니 관리 구현

```javascript
// BH Sound Module — 동시 발음 관리 (v1.2)
var BH_POLYPHONY_LIMIT = 12;        // 동시 최대 발음 수
var BH_activeSounds   = [];         // 현재 재생 중 사운드 추적

// Compressor (마스터 버스) — 전체 사운드 레벨 보정
function BH_getMasterBus() {
  if (window._BH_MasterBus) return window._BH_MasterBus;
  var ctx  = BH_getCtx();
  var comp = ctx.createDynamicsCompressor();
  comp.threshold.value = -18;  // dB
  comp.knee.value      = 6;
  comp.ratio.value     = 3;
  comp.attack.value    = 0.01;
  comp.release.value   = 0.1;
  comp.connect(ctx.destination);
  window._BH_MasterBus = comp;
  return comp;
}

// 폴리포니 한계 초과 시 가장 오래된 사운드 강제 종료
function BH_managePolyphony() {
  BH_activeSounds = BH_activeSounds.filter(function(s) {
    return s.node.playbackState !== 3; // FINISHED_STATE
  });
  if (BH_activeSounds.length >= BH_POLYPHONY_LIMIT) {
    var oldest = BH_activeSounds.shift();
    try { oldest.node.stop(); } catch(e) {}
  }
}

// 사운드 재생 래퍼 (폴리포니 체크 포함)
function BH_playSound(freq, type, A, D, S, R, dur) {
  if (window.BH_SoundMuted) return;
  BH_managePolyphony();
  var ctx  = BH_getCtx();
  var bus  = BH_getMasterBus();
  var gain = BH_createADSR(freq, type, A, D, S, R, dur);
  // BH_createADSR 내부에서 gain.connect(ctx.destination) 하던 것을
  // gain.connect(bus) 로 교체 — Compressor 경유
  BH_activeSounds.push({ node: gain, startedAt: Date.now() });
}
```

### 화투 게임 사운드 이벤트 우선순위

| 우선순위 | 이벤트 | 사운드 | 중복 허용 |
|---|---|---|---|
| 최고 | 족보 완성 (홍단·청단 등) | `BH_playJokbo()` | ❌ 단일 |
| 높음 | 매칭 성공 | `BH_playCardMatch()` | ✅ 2중 |
| 보통 | 카드 탭/배치 | `BH_playCardTap()` | ✅ 4중 |
| 낮음 | AI 턴 | `BH_playAITurn()` | ❌ 단일 |
| 배경 | BGM (선택사항) | GainNode loop | ❌ 단일 |

> ✅ `BH_playJokbo()` 재생 중에는 다른 사운드 1초간 duck (GainNode gain = 0.2)
> ✅ 뮤트 토글: `window.BH_SoundMuted = !window.BH_SoundMuted` — 저장: localStorage

### Audio Ducking (중요 사운드 강조)

```javascript
function BH_duckOtherSounds(durMs) {
  // 족보 사운드 재생 시 다른 게인 임시 감소
  var ctx = BH_getCtx();
  var bus = BH_getMasterBus();
  bus.gain.setTargetAtTime(0.2, ctx.currentTime, 0.05);       // 빠르게 감소
  bus.gain.setTargetAtTime(1.0, ctx.currentTime + durMs/1000, 0.3); // 서서히 복구
}
```


---

## 🎵 배경음악(BGM) 구조 설계 ★ v1.3 신설

**방침**: 배경음악은 선택(기본 OFF). Web Audio API Oscillator 기반 — 외부 파일 없음 (무료·저작권 0).
**스타일**: 일본 전통 음계(요나누키 음계) 기반 잔잔한 멜로디 → 화투 분위기 연출.

### 요나누키 음계 (Yona Nuki Scale)

```
요나누키 단음계: C D Eb G Ab (4·7번째 음 제거 — 한국·일본 전통 감성)
주파수(Hz):      261.6 293.7 311.1 392.0 415.3
```

### BGM 루프 구현

```javascript
// BH Sound Module — BGM 루프 (v1.3)
var BH_BGM_NOTES   = [261.6, 293.7, 311.1, 392.0, 415.3, 392.0, 311.1, 293.7];
var BH_BGM_DURS    = [0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5]; // 각 음 길이(초)
var BH_BGM_Timer   = null;
var BH_BGM_Playing = false;

function BH_playBGMNote(noteIdx) {
  if (!BH_BGM_Playing) return;
  var ctx  = BH_getCtx();
  var bus  = BH_getMasterBus ? BH_getMasterBus() : ctx.destination;
  var freq = BH_BGM_NOTES[noteIdx % BH_BGM_NOTES.length];
  var dur  = BH_BGM_DURS[noteIdx  % BH_BGM_DURS.length];

  var osc  = ctx.createOscillator();
  var gain = ctx.createGain();
  osc.type = 'triangle';         // 부드러운 음색
  osc.frequency.value = freq;
  gain.gain.setValueAtTime(0.06, ctx.currentTime);          // 매우 작게
  gain.gain.linearRampToValueAtTime(0.04, ctx.currentTime + dur * 0.8);
  gain.gain.linearRampToValueAtTime(0,    ctx.currentTime + dur);
  osc.connect(gain); gain.connect(bus);
  osc.start(ctx.currentTime);
  osc.stop(ctx.currentTime + dur);

  // 다음 음표 예약
  BH_BGM_Timer = setTimeout(function() {
    BH_playBGMNote(noteIdx + 1);
  }, dur * 1000);
}

function BH_startBGM() {
  if (BH_BGM_Playing || window.BH_SoundMuted) return;
  BH_BGM_Playing = true;
  BH_playBGMNote(0);
}

function BH_stopBGM() {
  BH_BGM_Playing = false;
  if (BH_BGM_Timer) clearTimeout(BH_BGM_Timer);
}

// 토글
function BH_toggleBGM() {
  BH_BGM_Playing ? BH_stopBGM() : BH_startBGM();
}
```

### BGM 이벤트 연동

| 게임 상태 | BGM 행동 |
|---|---|
| 게임 시작 (사용자 클릭 후) | `BH_startBGM()` |
| 족보 완성 효과음 재생 중 | `BH_duckOtherSounds(2000)` — BGM 2초간 감소 |
| 게임 종료 (SCORING 상태) | `BH_stopBGM()` |
| 뮤트 토글 | `BH_stopBGM()` 또는 `window.BH_SoundMuted` 확인 |

> ✅ BGM gain 0.06 — 효과음(0.3~0.8)보다 훨씬 작게 설정해 게임 집중 방해 최소화
> ✅ triangle 파형 — sine보다 풍성, square보다 부드러운 전통 악기 느낌
> ✅ 외부 오디오 파일 없음 — 저작권·로딩 이슈 완전 제거


---

## BGM 2악장 — 게임 중 긴장감 v1.4 신설

**설계**: 덱 남은 장수가 10장 이하가 되면 BGM 속도 1.3배 + 음계 단2도 상승 → 긴장감 연출.

```javascript
var BH_BGM_BASE_DUR = 0.5;  // 기본 템포
var BH_BGM_TENSE_DUR = 0.35;  // 긴장 템포 (빠르게)

// 덱 10장 이하 시 BGM 전환 호출
function BH_updateBGMTension() {
  var deckCount = BH_GS.deck.length;
  if (deckCount <= 10 && !BH_BGM_Tense) {
    BH_BGM_Tense = true;
    // 음정 반음 위로 (요나누키 단음계 × 1.059)
    BH_BGM_NOTES = BH_BGM_NOTES.map(function(f) { return f * 1.059; });
    BH_BGM_DURS  = BH_BGM_DURS.map(function()  { return BH_BGM_TENSE_DUR; });
  }
}
var BH_BGM_Tense = false;

// BH_flipFromDeck 호출 후 BH_updateBGMTension() 추가
```

> ✅ 음정 상승 계수 1.059 = 반음(semitone) — 음악적으로 정확한 긴장감 전환
> ✅ 게임 재시작 시 BH_BGM_Tense = false; BH_BGM_NOTES 원상 복구

---

## 🎼 BH_crossfadeBGM — BGM 2악장 크로스페이드 전환 v1.5 신설

**문제**: BGM_NOTES·DURS 즉시 변경 시 → 음악이 갑자기 끊기며 전환 → UX 어색  
**해결**: GainNode 페이드 아웃(1.5초) + 신규 BGM 페이드 인(1.5초) 오버랩

```javascript
// === BH_crossfadeBGM ===
// @param {boolean} toTense — true=2악장(긴장), false=1악장(일반)
// @param {number}  fadeDur — 크로스페이드 총 시간(초), 기본 3.0

var BH_BGM_BASE_NOTES  = [261.6, 293.7, 311.1, 392.0, 415.3, 392.0, 311.1, 293.7];
var BH_BGM_BASE_DURS   = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5];
var BH_BGM_TENSE_NOTES = BH_BGM_BASE_NOTES.map(function(f){ return f * 1.059; });
var BH_BGM_TENSE_DURS  = [0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35];

function BH_crossfadeBGM(toTense, fadeDur) {
  fadeDur = fadeDur || 3.0;
  var ctx = window.BH_AudioContext;
  if (!ctx || window.BH_SoundMuted) return;

  // 1) 현재 BGM GainNode 페이드 아웃
  var currentGain = window.BH_BGM_GainNode;
  if (currentGain) {
    currentGain.gain.setValueAtTime(currentGain.gain.value, ctx.currentTime);
    currentGain.gain.linearRampToValueAtTime(0, ctx.currentTime + fadeDur / 2);
    // 페이드 아웃 완료 후 현재 BGM 중지
    setTimeout(function() {
      BH_stopBGM();
    }, (fadeDur / 2) * 1000);
  }

  // 2) 새 BGM 페이드 인 (페이드 아웃 중반부터 시작)
  setTimeout(function() {
    // 음계·템포 전환
    BH_BGM_NOTES = toTense ? BH_BGM_TENSE_NOTES.slice() : BH_BGM_BASE_NOTES.slice();
    BH_BGM_DURS  = toTense ? BH_BGM_TENSE_DURS.slice()  : BH_BGM_BASE_DURS.slice();
    // 새 GainNode gain 0에서 시작 → 페이드 인
    BH_BGM_Playing = false;  // startBGM 내부 중복 방지 초기화
    BH_startBGM();
    var newGain = window.BH_BGM_GainNode;
    if (newGain) {
      newGain.gain.setValueAtTime(0, ctx.currentTime);
      newGain.gain.linearRampToValueAtTime(0.06, ctx.currentTime + fadeDur / 2);
    }
  }, (fadeDur / 4) * 1000);  // 페이드 아웃 1/4 지점에서 새 BGM 시작
}

// BH_startBGM에서 GainNode를 전역으로 저장하도록 수정
// (기존 BH_startBGM 내부):
// var gainNode = ctx.createGain();
// gainNode.gain.value = 0.06;
// window.BH_BGM_GainNode = gainNode;  // ← 이 줄 추가
```

**호출 시점 연동**

```javascript
// FSM PLAYER_FLIP 또는 AI_TURN 후 덱 감소 체크
function BH_checkAndUpdateBGM() {
  if (!BH_BGM_Tense && BH_GS.deck.length <= 10) {
    BH_BGM_Tense = true;
    BH_crossfadeBGM(true, 3.0);  // 2악장으로 부드럽게 전환
  }
}

// 게임 재시작 시 1악장으로 복귀
function BH_resetBGM() {
  if (BH_BGM_Tense) {
    BH_BGM_Tense = false;
    BH_crossfadeBGM(false, 2.0);  // 1악장으로 복귀 (빠른 전환)
  } else {
    BH_stopBGM();
    BH_startBGM();
  }
}
```

---

## 🔊 효과음 우선순위 큐 — BH_SoundQueue v1.5 신설

**문제**: 여러 효과음이 동시에 트리거될 때 (족보 획득 + 카드 매칭) → 사운드 겹침 혼란  
**해결**: 우선순위 큐 → 높은 우선순위 사운드가 낮은 것을 ducking(음소거 감쇠)

```javascript
// === 우선순위 정의 ===
var BH_SOUND_PRIORITY = {
  jokbo:   10,  // 족보 획득 (최우선) — 팡파레
  badge:    9,  // 배지 획득
  win:      8,  // 승리
  lose:     7,  // 패배
  flip:     5,  // 덱 뒤집기
  match:    4,  // 카드 매칭
  select:   3,  // 카드 선택
  hint:     2,  // 힌트 사용
  tick:     1,  // BGM 음표 (최저)
};

// === 큐 관리 ===
var BH_SoundQueue = [];
var BH_SoundPlaying = false;

function BH_queueSound(type, playFn) {
  var priority = BH_SOUND_PRIORITY[type] || 0;
  BH_SoundQueue.push({ priority: priority, play: playFn });
  BH_SoundQueue.sort(function(a, b) { return b.priority - a.priority; }); // 내림차순
  BH_processQueue();
}

function BH_processQueue() {
  if (BH_SoundPlaying || BH_SoundQueue.length === 0) return;
  var next = BH_SoundQueue.shift();
  BH_SoundPlaying = true;
  // 높은 우선순위 사운드 재생 시 BGM ducking
  if (next.priority >= 7) {
    BH_duckOtherSounds(true);  // BGM 볼륨 50% 감쇠
  }
  next.play(function onComplete() {
    BH_SoundPlaying = false;
    if (next.priority >= 7) {
      BH_duckOtherSounds(false);  // BGM 볼륨 복구
    }
    setTimeout(BH_processQueue, 50);  // 50ms 후 다음 사운드
  });
}

// 사용 예시
// BH_queueSound('jokbo', function(done) { BH_playJokboSound('godori', done); });
// BH_queueSound('match', function(done) { BH_playMatchSound(done); });
```

**BH_duckOtherSounds 개선 (페이드 반영)**

```javascript
function BH_duckOtherSounds(duck) {
  var gain = window.BH_BGM_GainNode;
  if (!gain) return;
  var ctx = window.BH_AudioContext;
  if (!ctx) return;
  var targetGain = duck ? 0.015 : 0.06;  // ducking: 75% 감쇠
  gain.gain.setValueAtTime(gain.gain.value, ctx.currentTime);
  gain.gain.linearRampToValueAtTime(targetGain, ctx.currentTime + 0.1);  // 100ms 페이드
}
```

> ✅ 족보 획득 팡파레 = priority 10 → 다른 모든 사운드보다 먼저 재생  
> ✅ BGM ducking 100ms 페이드 → 갑작스러운 볼륨 변화 없음  
> ✅ setTimeout(50ms) 간격 → 연속 사운드 자연스러운 분리

---

## 🔇 뮤트 버튼 토글 표준 v1.5 신설

```javascript
// 뮤트 토글 — BGM + 효과음 동시 제어
function BH_toggleMute() {
  window.BH_SoundMuted = !window.BH_SoundMuted;
  try { localStorage.setItem('BH_muted', BH_SoundMuted ? '1' : '0'); } catch(e) {}
  if (BH_SoundMuted) {
    // BGM 즉시 중지
    if (window.BH_BGM_GainNode) {
      window.BH_BGM_GainNode.gain.value = 0;
      BH_BGM_Playing = false;
    }
    // 큐 비우기
    BH_SoundQueue = [];
    BH_SoundPlaying = false;
  } else {
    // 뮤트 해제 → BGM 재시작
    BH_startBGM();
  }
  // UI 버튼 aria-label 갱신
  var btn = document.getElementById('BH_btn_mute');
  if (btn) {
    btn.setAttribute('aria-label', BH_SoundMuted ? '소리 켜기' : '소리 끄기');
    btn.textContent = BH_SoundMuted ? '🔇' : '🔊';
  }
}
```

> ✅ 뮤트 상태 localStorage 저장 — 재방문 시 이전 설정 유지  
> ✅ 뮤트 해제 시 BGM 자동 재시작 — 사용자 경험 연속성  
> ✅ aria-label 갱신 — 스크린 리더 접근성 (WCAG 2.1 준수)
