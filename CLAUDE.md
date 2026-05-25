# CLAUDE.md

> **PROJECT_ID: `brain_health_1.0`** — 이 저장소(`C:\Claude_code\`)의 모든 `.md`·`xlsx`·스냅샷·핸드오프·메모리는 **brain_health(뇌건강 블로그) 전용**입니다. 타 프로젝트(`dailypickhub` 등) 식별자가 본문에 등장하면 = 교차 오염 → 즉시 정화 + 사용자 보고. (상세 룰: 아래 `### 교차 프로젝트 오염 방지`)

---
## 🔴 라이브 PATCH 전 로컬 HTML 검증 필수 (★ 2026-05-25 신설)

**사고 배경**: 2026-05-25 Post #7 카드 인식 애니메이션 FSM 통합 라이브 사고. 로컬 검증 0회 상태로 라이브 PATCH 실행 → "1월 광 카드 잔존" 버그 미검출 → PATCH 4건 연쇄 대응 → 진짜 원인(FSM 진입점 결함) 미해결 → 사용자 GUI 리비전 복원으로 라이브 정상화.

| 규칙 | 내용 |
|---|---|
| **로컬 검증 필수** | `widgets/post*_widget.html` 코드 변경 시 라이브 PATCH 전 로컬 wrapper.html 환경에서 직접 플레이 검증 필수 |
| **PASS 기준** | 페이지 진입 → 난이도 모달 정상 출현 → 난이도 선택 → 게임 진행 → 광 카드 포함 전체 카드 정상 동작 (FAIL 패턴 0건) |
| **환경 미구축 시** | 로컬 검증 환경(wrapper.html)이 구축되기 전까지 게임 위젯 라이브 PATCH 임시 보류 |
| **PASS 첨부 의무** | game·qa 로컬 검증 PASS 결과 없이 dev에 라이브 PATCH 위임 금지 |

> ⚠️ 라이브 PATCH 후 버그 발견 시 연쇄 PATCH 시도 금지 — 즉시 멈추고 로컬에서 원인 특정 후 재시도

---
## 🔴 git 운영 룰 — Windows 전용 실행 (★ 2026-05-25 확정)

**근본 원인**: Linux 샌드박스(Cowork)에서 git 실행 시 `.git/index.lock`이 NTFS 마운트 권한 구조상 삭제 불가 → 연속 git 명령 실행 불가.

| 규칙 | 내용 |
|---|---|
| ❌ **Cowork(Linux 샌드박스) git 금지** | git add·commit·push 등 모든 git 명령을 Cowork에서 실행 금지 |
| ✅ **Claude Code(Windows) 전용** | git 작업은 반드시 Claude Code(Antigravity) 또는 PowerShell/Git Bash에서 실행 |
| **lock 파일 발생 시** | PowerShell: `del .git\index.lock`, `del .git\config.lock` 후 재시도 |
| **마운트 캐시** | Cowork bash에서 파일 크기·내용이 Windows 실제와 다를 수 있음 — git 상태 확인은 Claude Code에서 |

---
## 🔴 위젯 파일 단일 정본 룰 (★ 2026-05-25 확정)

**사고 원인**: `post7_widget_v5b.html` 등 버전 suffix 파일이 난립 → game 에이전트가 수정일 기준으로 잘못된 구버전을 베이스로 선택 → 커스텀 사항 전체 유실.

| 규칙 | 내용 |
|---|---|
| **정본 파일명 고정** | `widgets/post{N}_widget.html` — 버전 suffix(v1·v2·v5b 등) 없이 단일 파일명 유지 |
| **버전 관리 = git** | 버전 히스토리는 git 커밋으로 관리. 파일명으로 버전 구분 금지 |
| **베이스 파일 기준** | suffix 없는 `post{N}_widget.html`이 항상 정본. 수정일·파일명 suffix 신뢰 금지 |
| **작업 전 확인** | game·dev 에이전트는 수정 전 반드시 정본 파일명 기준으로 작업 진입 |

---
## 🔴 핵심 상수 — 절대 변경 금지 (★ 2026-05-18 신설)

| 항목 | 값 | 비고 |
|---|---|---|
| **사이트 URL** | `https://neuralcare.co.kr` | 하이픈(-) 없음. `neural-care`는 오타 |
| **WP 관리자** | `https://neuralcare.co.kr/wp-admin/` | |
| **REST API 베이스** | `https://neuralcare.co.kr/wp-json/wp/v2/` | |
| **Nonce 발급** | `https://neuralcare.co.kr/wp-admin/admin-ajax.php?action=rest-nonce` | 세션마다 재발급 |

> ⚠️ `neural-care.co.kr`(하이픈 포함)은 **존재하지 않는 도메인**. 이 패턴이 어디서든 등장하면 즉시 정정할 것.

---
## 🔴 추정 금지 룰 — 미확인 항목 실측 의무 (★ 2026-05-24 신설)

**근본 원인**: 핸드오프에 "추정" 기재 → 다음 세션이 가정 그대로 작업 진입 → 엉뚱한 대상 수정.

| 규칙 | 내용 |
|---|---|
| **핸드오프 "추정" 금지** | 미확인 항목은 "추정" 표현 금지. 반드시 `⚠️ 미확인 — 다음 세션 실측 필수: [확인 방법]` 형식으로 명시 |
| **세션 시작 실측 의무** | 핸드오프에 "미확인" 항목 있으면 첫 번째 행동은 실측 확인. 가정으로 작업 진입 금지 |
| **이미지 버그 전수 확인** | 이미지 Mojibake 등 이미지 관련 버그 신고 시 → 해당 포스트의 **전체 이미지 목록** 먼저 확인 후 깨진 이미지 특정, 그 다음 수정 착수 |

> ⚠️ 사고 사례(2026-05-24): 핸드오프 "p6c01 추정" → p6c01 수정 → 실제 깨진 이미지는 p6c02였음

---
---
## 🔴 발행 패키지 업로드 검증 — 핸드오프 ✅ 기재 전 필수 (★ 2026-05-20 신설, 2026-05-20 개정)

**포스트 업로드 완료 후 아래 항목 PASS 후에만 핸드오프 ✅ 기재 허용. 예외 없음.**

| 항목 | 확인 내용 | FAIL 시 |
|---|---|---|
| S1 | **본문 텍스트 있음** — entry-content innerText 500자 이상 | dev에 본문 업로드 지시 |
| S3 | **한글 Mojibake 0건** — get_page_text에 깨진 문자 패턴 0건 | dev에 위젯 인코딩 재업로드 지시 |
| SW | **위젯 함수 로드** — `typeof BH_[포스트별 게임함수명] === "function"` | dev에 위젯 재업로드 지시 |

> S1·S3·SW 전부 PASS 후에만 핸드오프 ✅ 기재 허용.
> SW 함수명은 포스트마다 다름 — game_planner 기획서 [검수 식별자] 항목에서 확인.
> "업로드 완료" = 본문 + 위젯 둘 다 WP 업로드. 위젯만 올리면 미완료.
> **S1 예외**: `/brain-games/[게임명]/` 형태의 게임 전용 허브 페이지는 아티클 본문이 없는 설계이므로 S1 적용 제외. SW·S3만 필수. (확정 2026-05-20)

**개정 배경**: S2(BH_startWithDiff)·S4(.BH_card)는 Post #7 민화투 전용 식별자 — 10개 에이전트 라운드테이블 만장일치로 삭제 결정(2026-05-20).

## 🔴 WP CSS 특이성(Specificity) 버그 — 게임 모달 display 제어 (★ 2026-05-20 확정)

**근본 원인**: WordPress 테마 CSS에 `.BH_difficulty_modal { display:flex }` 같은 클래스 선택자 규칙이 있으면, HTML `[hidden]` 속성(`display:none` 적용)을 **CSS 특이성에서 이긴다**. 결과: 난이도 선택 모달이 사라지지 않아 게임 시작 불가.

| 규칙 | 내용 |
|---|---|
| ❌ **setAttribute('hidden') 금지** | 게임 모달(BH_diff_modal·BH_game_board·BH_result_modal)에 `[hidden]` 속성 방식 사용 금지 |
| ✅ **style.display 직접 제어 필수** | `element.style.display='none'` (숨김) / `element.style.display=''` 또는 `'flex'` (표시) |
| **적용 대상** | BH_diff_modal · BH_game_board · BH_result_modal — 3개 모달 전부 |
| **예외** | `BH_how_panel` (설명 토글)은 테마 CSS 충돌 없어 `setAttribute('hidden')` 허용 |
| **검증** | 미리보기에서 난이도 선택 후 게임 보드 전환 정상 여부 확인 필수 |

```js
// ✅ 올바른 방식
dm.style.display = 'none';   // 모달 숨김
gb.style.display = '';        // 게임 보드 표시
rm.style.display = 'flex';   // 결과 모달 표시

// ❌ 잘못된 방식 (WP 테마 CSS에 override 당함)
dm.setAttribute('hidden', '');
dm.removeAttribute('hidden');
```

> ⚠️ WP 테마마다 적용된 CSS 규칙이 다를 수 있으므로 `style.display` 직접 제어가 항상 안전

---
## 🔴 WP featured_media 렌더링 위치 — 이미지 디버깅 필수 확인 (★ 2026-05-23 확정)

**근본 원인**: WP `featured_media`(대표 이미지)는 포스트 본문(`content.raw`)과 **완전히 분리된 별도 메타데이터 필드**로, 테마 PHP 템플릿이 `.entry-content` **밖**에 자동 렌더링한다. content.raw 검색·`.entry-content` DOM 탐색으로는 절대 검출 불가.

| 규칙 | 내용 |
|---|---|
| **이미지 디버깅 1순위** | 페이지에 이미지가 보이는데 `.entry-content` 안에 없으면 → `featured_media` 필드 먼저 확인 |
| **확인 방법** | `GET /wp-json/wp/v2/pages/{ID}?context=edit` → `featured_media` 값 확인 |
| **제거 방법** | `PATCH /wp-json/wp/v2/pages/{ID}` + `{"featured_media": 0}` |
| **렌더링 위치** | 테마 템플릿 → 헤더 아래, `.entry-content` 위 (테마마다 다름) |

> ⚠️ content.raw에 이미지 없음 = 이미지 없음이 **아님**. featured_media 별도 확인 필수.
> 실제 사례: 2026-05-23 Page #303 민화투 게임 허브 — featured_media:276이 게임 위에 카드 이미지 자동 표시, 에이전트 3개가 "없다" 오진.

## 🔴 CSS position:absolute 자식 + overflow:hidden 수축 함정 (★ 2026-05-23 확정)

**근본 원인**: 게임 모달이 `position:absolute`이면 부모 컨테이너가 자식 높이를 인식하지 못해 수축(shrink). `overflow:hidden`과 결합 시 모달이 DOM에는 존재하지만 시각적으로 잘려 사용자 눈에 안 보임.

| 규칙 | 내용 |
|---|---|
| **모달 컨테이너 min-height 필수** | `position:absolute` 자식(모달)을 포함하는 부모에 반드시 `min-height` 명시 |
| **진단 방법** | `el.offsetHeight` vs `el.scrollHeight` 비교 — offsetHeight < scrollHeight이면 잘림 |
| **해결** | 부모 CSS에 `min-height: {모달높이+여유}px` 추가 |
| **적용 사례** | `.BH_hwatu_wrap { min-height:420px; overflow:hidden; }` |

> ⚠️ 증상: "게임이 시작 안 됨" / "버튼이 안 보임" — 실제론 DOM에 존재, 시각적 잘림
> 실제 사례: 2026-05-23 `.BH_hwatu_wrap` height 102px 수축 → 난이도 모달 400px 잘림

---
## 🔴 WP wp_staticize_emoji() 핵심 룰 — JS 내 이모지 금지 (★ 2026-05-19 확정)

**근본 원인**: WordPress `wp_staticize_emoji()` 필터는 `<script>` 태그 **안쪽의 이모지 문자**를 `<img>` 태그로 교체한다. 결과: JS SyntaxError, 게임 작동 불가.

| 규칙 | 내용 |
|---|---|
| **JS 내 이모지 절대 금지** | `<script>` 블록 안에 이모지 문자 직접 사용 금지 |
| **대체 방법** | ES6 Unicode escape: `\u{1F3AE}` 형식으로 교체 |
| **Python 변환** | `re.sub(emoji_pattern, lambda m: '\\u{'+hex(ord(m.group()))[2:].upper()+'}', js_code)` |
| **검증** | WP 저장 후 브라우저 console → SyntaxError 0건 확인 |
| **적용 대상** | 게임 위젯 JS, 인라인 스크립트 모두 해당 |

> ⚠️ `typeof BH_startWithDiff === 'function'` 체크로 게임 로드 성공 여부 빠르게 검증 가능

---
## 🔴 WP wpautop 핵심 룰 — wp:html 블록 내 CSS/JS (★ 2026-05-18 확정)

**근본 원인**: WordPress `wpautop()` 필터는 `<!-- wp:html -->` 블록 내 `<style>`, `<script>` 태그 **안쪽 내용도** 처리한다.
줄바꿈 → `<br />`, 빈 줄 → `<p>`, `---` 줄 → `<hr>`. CSS 파싱 붕괴·JS SyntaxError 유발.

| 규칙 | 내용 |
|---|---|
| **style 단일 행** | `<!-- wp:html -->` 내 `<style>` CSS는 개행 없이 단일 행으로 저장 필수 |
| **script 단일 행** | `<!-- wp:html -->` 내 `<script>` JS는 개행 없이 단일 행으로 저장 필수 |
| **wp:html 수동 포함** | PUT 시 `<!-- wp:html -->` ~ `<!-- /wp:html -->` 마커를 raw content에 직접 포함해야 함 |
| **위젯 수정 절차** | 원본 `.html` 파일 → Python minify → wp:html 블록 전체 교체 PUT |
| **검증** | PUT 후 GET raw content → script/style 내 `<br>`, `<p>`, `<hr>` 0건 확인 |

> ❌ **절대 금지**: `<!-- wp:html --> 패턴은 WP 저장 시 자동 부착` — 이는 오정보. 반드시 수동 포함해야 함.

---
## 🔴 WP REST API 타겟 PATCH — 대용량 콘텐츠 수정 안전 절차 (★ 2026-05-20 신설)

**근본 원인**: 대용량 콘텐츠(30KB+)를 통째로 PATCH할 경우, 로컬 보관 내용이 WP 최신 상태와 다를 수 있음 → 이전 버전 덮어쓰기 또는 문자 오염 위험.

| 규칙 | 내용 |
|---|---|
| **원본 먼저 GET** | 수정 전 반드시 `?context=edit`로 raw content 실시간 GET |
| **타겟 replace** | `rawContent.replace("구문자", "신문자")` — 변경 대상만 교체 |
| **PATCH 전 검증** | replace 후 `indexOf("구문자") === -1` 확인 필수 |
| **전체 재업로드 금지** | 로컬 `.html` 파일 그대로 PATCH 금지 (stale data 위험) |
| **예외** | 위젯 전체 교체(신규 버전 배포) 시는 Python minify 후 전체 PATCH 허용 |

**사고 배경**: 2026-05-20 잘못된 base64 청크 패치로 `!`(code 33) → `'`(code 39) 단 1글자 오염 → `SyntaxError: Unexpected identifier 'BH_muted'` 발생.

---
## 🔴 Base64 위젯 UTF-8 디코딩 룰 — atob() Mojibake 방지 (★ 2026-05-20 신설)

**근본 원인**: JavaScript `atob()` 함수는 Base64 → Latin-1(ISO-8859-1)로 디코딩한다. 한글·이모지 등 멀티바이트 문자를 포함한 위젯을 Base64 인코딩한 뒤 `atob()`로만 복원하면 Mojibake(깨진 문자) 발생.

| 규칙 | 내용 |
|---|---|
| ❌ **`atob()` 단독 사용 금지** | 한글·이모지 포함 Base64 위젯에 `atob()` 직접 사용 금지 |
| ✅ **TextDecoder UTF-8 필수** | `new TextDecoder('utf-8').decode(Uint8Array.from(atob(b64), c=>c.charCodeAt(0)))` |
| **window._wg 전처리** | 청크 주입 후 공백 혼입 방지 → `window._wg.replace(/\s/g,'')` 전처리 필수 |
| **검증** | 브라우저에서 한글 카드명·이모지 정상 렌더링 확인 |

```js
// ✅ 올바른 방식 (한글/이모지 포함 위젯 복원)
const raw = new TextDecoder('utf-8').decode(
  Uint8Array.from(atob(window._wg.replace(/\s/g,'')), c => c.charCodeAt(0))
);

// ❌ 잘못된 방식 (Latin-1 해석 → Mojibake)
const raw = atob(window._wg);
```

**사고 배경**: 2026-05-20 Post #281 민화투 위젯에서 화투 카드명(한글)·족보 이모지가 전부 깨져 출력. `atob()` Latin-1 해석이 원인. TextDecoder 패턴으로 전환 후 해결.

---
## 🔴 JS SyntaxError CharSum 세그먼트 디버깅 기법 (★ 2026-05-20 신설)

**용도**: WP-저장 스크립트 vs Python-생성 스크립트 간 미세 차이(1~6글자)를 빠르게 찾을 때.

**절차**:
1. **Python bash** — 기준 스크립트의 1000자 단위 CharSum 계산
   ```python
   for start in range(0, len(sc), 1000):
       seg = sc[start:start+1000]
       print(f"[{start}-{start+len(seg)}]: {sum(ord(c) for c in seg)}")
   ```
2. **Chrome JS** — DOM `<script>` 추출 후 동일하게 계산
   ```js
   var sc = document.querySelector('script').textContent; // BH_muted 포함 스크립트
   for (var s=0; s<sc.length; s+=1000) {
     var seg=sc.substring(s,s+1000), sum=0;
     for(var i=0;i<seg.length;i++) sum+=seg.charCodeAt(i);
     console.log(s+'-'+(s+seg.length)+': '+sum);
   }
   ```
3. **비교** — 합계가 다른 세그먼트 특정 → 100자 → 10자 → 문자 코드로 좁히기
4. **타겟 PATCH** — 정확한 위치 확인 후 단일 문자 replace + PATCH

> ⚠️ Chrome `javascript_tool` 결과에 특수문자(쿼리스트링·쿠키 패턴) 포함 시 차단 → 숫자 배열로만 반환

---
## 🖼️ 카드 이미지 2-버전 분리 정책 (★ 2026-05-18 확정)

**결정 배경**: 배경 제거·폰트 확대 방향에 전 에이전트 찬성. ads 에이전트 제안 적극 수용 — 용도별 2버전 분리.

| 버전 | 용도 | 배경 | 폰트 | 파일명 규칙 |
|---|---|---|---|---|
| **본문용 (body)** | WP 본문 figure 블록 삽입 | 흰 배경 (`#FFFFFF`) + 테두리선 | 확대 (카드 22~24px+) | `p{N}c0{n}_body.png` |
| **OG용 (og)** | 소셜 공유 대표 이미지 / Rank Math OG | 원래 컬러 배경 (청록 계열) 유지 | 기존 비율 | `p{N}c0{n}_og.png` |

**적용 규칙**:
- design 에이전트는 모든 카드 이미지를 **2버전 동시 제작** (본문용 + OG용)
- WP 미디어 업로드: **본문용 → 본문 `figure 블록`만** / **OG용 → `featured_media` + Rank Math OG 이미지 필드** (★ featured_media = OG 버전)
- 본문용: 흰 배경 위 텍스트 색은 진한 네이비·차콜(#1a2b3c 또는 동급) — WCAG AA 대비비 4.5:1 이상 필수
- OG용: 소셜 플랫폼 배경 색상 간섭 방지 목적 — 컬러 배경 유지
- dev 에이전트: 신규 업로드 후 `figure 블록 mediaId` 교체 방식 사용 (WP REST API 미디어 덮어쓰기 지원 X)

> ⚠️ 본문용·OG용 혼용 금지. 흰 배경 카드를 OG로 올리면 소셜 공유 시 배경 공백으로 표시됨.

---
## 🔴 wp:image 블록 이중 저장 룰 — 이미지 교체 시 필수 (★ 2026-05-18 확정)

**근본 원인**: Gutenberg `wp:image` 블록은 이미지 정보를 **두 곳에 독립적으로** 저장한다. WP는 preview 시 `<img src>` URL을 직접 렌더링하므로, ID만 교체하면 구 이미지가 그대로 출력됨.

| 저장 위치 | 형식 | 역할 |
|---|---|---|
| 블록 속성 | `<!-- wp:image {"id":248,...} -->` | 미디어 라이브러리 참조 ID |
| 내부 HTML | `<figure><img src="URL" class="wp-image-248"...>` | 실제 렌더링에 사용되는 URL |

**이미지 교체 시 반드시 둘 다 수정**:
```
1. 블록 속성 id 숫자 교체: {"id": OLD} → {"id": NEW}
2. <img src="OLD_URL"> → <img src="NEW_URL">
3. class="wp-image-OLD" → class="wp-image-NEW"
```

**QA 검증 항목 (이미지 교체 후 GET 재확인 필수)**:
- `wp:image {"id":N}` 패턴의 N = 새 미디어 ID ✅
- `<img src="...">` URL이 새 파일 URL ✅ ← **이전에 빠졌던 검증 항목**
- `wp-image-N` class N = 새 미디어 ID ✅

> ❌ **절대 금지**: ID만 교체하고 src URL 미교체 → 미리보기·실제 페이지에서 구 이미지 렌더링됨.

---


Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---

## 프로젝트 규칙 (brain_health_1.0 / 뇌건강 블로그)

위 generic 룰 위에 적용되는 이 프로젝트 운영 룰. 메모리(`feedback_*.md`)와 동기화된 이중 안전장치.

### 교차 프로젝트 오염 방지 (★ 2026-05-14 신설 — dailypickhub 역수입 사고 후)

brain_health는 멀티 프로젝트 환경의 하나. 타 프로젝트 작업물 유입을 구조적으로 차단한다.

- **세션 1:1 원칙**: 한 Claude 세션 = brain_health 전용. 타 프로젝트 작업 시 반드시 새 세션 (한 세션에서 두 프로젝트 동시 작업 금지)
- **타 프로젝트 식별자 금지**: `.md`·`xlsx`·핸드오프·스냅샷 본문에 다른 프로젝트명(`dailypickhub` 등)이 등장하면 = 오염. 발견 즉시 정화 + 사용자 보고
- **노하우 이식 = "복사" 금지**: 타 프로젝트의 좋은 노하우를 가져올 때는 통째 복사가 아니라 brain_health 언어로 **재작성**. "역수입"·"○○ 동기화" 같은 출처 표기 금지 — 흡수하려면 100% 자체 룰로
- **`.md` 수정 전 게이트**: 에이전트 `.md` 수정 직전, 해당 파일에 타 프로젝트 식별자가 있는지 grep 1회. 검출 시 수정 중단·정화 우선
- **정기 교차오염 감사**: 주 1회 또는 에이전트 `.md` 대규모 변경 후, 전체 `.md`·`xlsx` grep 감사 (타 프로젝트 식별자 0건 확인). `/cross-contamination-check` 슬래시 커맨드 활용
- **백업 위치**: 정화 작업 시 정화 전 상태를 `_archive/pre_decontamination_YYYY-MM-DD/`에 백업 (원상복구 안전장치)

### 사용자 소통
- **팀장 단일 창구**: 사용자 요청은 항상 팀장(`lead`) 에이전트 페르소나로 응답. 다른 10개 에이전트(라이터·디자인·디자인UI·개발·광고·게임·게임기획·QA·오프페이지·사운드)는 팀장 경유로만 호출
- **팀장 실행 금지 (하이브리드 금지)**: 팀장은 분석·위임·검토·종합·보고·룰 정합성 점검만 수행. 코드·디자인 자산·본문·검증 도구 실행은 10개 에이전트만 (lead.md v6.18 Critical 섹션 참조)
- **응답 언어**: 한국어
- **출력 형식**: 박스(═════) / 마크다운 표 / ✅⚠️❌ / 시점 1·2·3 형식 (lead.md 참조)
- **용어 자동 설명**: 백링크·SEO·광고 용어 첫 등장 시 1줄 설명 동반 (오너 비전문 가정)

### 🌐 Cowork mode 협업 모델 v1.0 (★ 2026-05-18 신설 / 2026-05-25 환경 결정 반영)

> 📌 **명칭 주의**: "Cowork mode"는 환경 이름이 아니라 **다중 에이전트 병렬 실행 모델** 이름. 본 모델은 Claude Code 단일 환경에서 그대로 적용됨. (사용자 결정 2026-05-25 — brain_health 워크플로우는 Claude Code 단일 환경 통합. Cowork 환경 분리 폐기)

**적용 환경**: Claude Code (Antigravity) 단일 환경 — Agent tool로 실제 분리 인스턴스 실행 가능  
**모델**: 작업 유형에 따라 두 가지 방식으로 분기하는 하이브리드 구조

#### 작업 유형별 실행 방식

| 작업 유형 | 방식 | 해당 에이전트 |
|---|---|---|
| **독립 실행 가능** | ✅ Agent tool → 실제 분리 인스턴스 | writer(초안) / game(위젯) / offpage(링크조사) / design(카드PNG) / design_ui(UI컴포넌트) / sound(효과음) / game_planner(기획서) / qa(검수) |
| **세션 의존** | 페르소나 전환 (단일 인스턴스) | dev(WP API·Chrome MCP) / ads(마커 배치) |
#### 🔴 구조적 한계 및 실질적 격리 (★ 2026-05-22 확정)

| 구분 | 내용 |
|---|---|
| **단일 인스턴스 한계** | lead·game·QA 등 모든 페르소나는 같은 Claude 인스턴스 — 기술적 역할 강제 불가 |
| **Agent tool = 실질적 격리** | game·QA 등을 Agent tool로 호출 시 진짜 분리 인스턴스 → 내부 규칙 준수 보장 |
| **lead 직접 실행** | 기술적으로 막을 수 없음 → 사용자 감독이 유일한 실질적 통제 수단 |
| **올바른 패턴** | 코드/검수 문제 발견 → lead 즉시 멈춤 → Agent tool로 해당 에이전트 호출 |



#### 페르소나 규율 (단일 인스턴스 전환 시 강제)
1. **페르소나 헤더 강제**: 작업마다 `[writer 페르소나 vX.XX]`, `[dev 페르소나 vX.XX]` 명시
2. **사전 Read 강제**: 해당 에이전트 `.md` 파일 Read 후 작업 시작 (생략 금지)
3. **자가점검 체크리스트** 응답에 명시 노출 (✅⚠️❌)
4. **lead 복귀**: 작업 종료 후 반드시 lead 페르소나로 복귀

#### Agent tool 표준 호출 규칙
- 각 에이전트 `.md`의 `## Agent tool 호출 표준` 섹션이 기준
- **입력**: STEP 4 브리프에서 해당 에이전트 필요 항목만 추출하여 전달
- **출력**: 아래 표준 경로에 파일 저장 → lead가 파일 존재 확인 후 다음 단계 진행

#### 표준 출력 파일 경로
| 에이전트 | 출력 파일 경로 |
|---|---|
| writer | `C:\Claude_code\drafts\post{N}_draft.md` |
| game | `C:\Claude_code\widgets\post{N}_widget.html` |
| offpage | `C:\Claude_code\research\post{N}_links.md` |
| qa | `C:\Claude_code\qa\post{N}_qa_report.md` |
| design | `C:\Claude_code\design\p{N}c01_body.png` ~ `p{N}c03_og.png` |
| design_ui | `C:\Claude_code\widgets\post{N}_ui.html` (또는 game에 직접 전달) |
| sound | game 에이전트에 BH Sound Module JS 블록 직접 전달 |
| game_planner | `C:\Claude_code\game_plans\post{N}_game_plan.md` |

#### 병렬 실행 맵 (STEP 5 기준)
```
[STEP 4 브리프 완료]
        ↓
┌──────────────────────────────────────────────────┐
│ Group A — 동시 실행 (브리프만 있으면 됨)          │
│  ① writer      → drafts/post{N}_draft.md        │
│  ② offpage     → research/post{N}_links.md      │
│  ③ game_planner→ game_plans/post{N}_game_plan.md│
│  ④ design_ui   → UI 컴포넌트 블록 (game에 전달) │
│  ⑤ sound       → 효과음 JS 모듈 (game에 전달)   │
└──────────────────────────────────────────────────┘
        ↓ Group A 전부 완료 확인 후
┌──────────────────────────────────────────────────┐
│ Group B — 초안·기획서 기반 실행                  │
│  ⑥ game   → widgets/post{N}_widget.html          │
│  ⑦ design → design/p{N}c01_body~og.png          │
│  ⑧ qa     → qa/post{N}_qa_report.md             │
└──────────────────────────────────────────────────┘
        ↓ Group B 전부 완료 확인 후
┌──────────────────────────────────────────────────┐
│ 순차 (세션 의존 — 페르소나 전환)                 │
│  ⑨ dev  → WP Draft API 업로드                   │
│  ⑩ 사용자 → WP 에디터 작업 → 수동 발행          │
└──────────────────────────────────────────────────┘
```

#### lead 오케스트레이션 책임
- STEP 4 브리프 완료 → Group A 에이전트 Agent tool 동시 호출
- Group A 파일 전부 존재 확인 → Group B 호출
- Group B 파일 전부 존재 확인 → dev 페르소나 전환 WP 업로드
- 전체 완료 → 발행 패키지 보고 (STEP 8)

### 수정 후 QA 의무 (★ 2026-05-18 신설)

**"어떤 수정이든 완료 직후 QA 검수 필수"** — 예외 없음.

| 수정 유형 | 예시 | QA 트리거 |
|---|---|---|
| 버그 수정 | `</script>` 복원, 블록 마커 추가 | 즉시 |
| 콘텐츠 수정 | 플레이스홀더 제거, 광고 마커 주석 처리, 이미지 삽입 | 즉시 |
| 코드 교체 | JS 로직 변경, CSS 수정 | 즉시 |
| 메타/설정 변경 | FK·슬러그·메타 디스크립션·featured_media 변경 | 즉시 |

- lead는 수정 작업 완료 직후 **반드시 qa 에이전트 검수** 지시
- 검수 완료(GET 재확인 PASS) 전에는 핸드오프 ✅ 기재 금지
- 검수 생략 = 미완료. "수정했다"는 보고만으로 ✅ 처리 불가

### 🔴 검수 요청 시 qa.md 의무 Read 규칙 (★ 2026-05-20 신설)

**사용자가 "검수해줘", "검수 진행", "리뷰해줘" 등 검수 관련 요청을 하면 반드시 아래 순서로 실행. 예외 없음.**

1. 즉시 `qa.md` Read
2. qa.md에 정의된 다중 에이전트 검수 루프 프로토콜대로 실행
3. 임의 수동 수정 금지

> ❌ **절대 금지**: qa.md 확인 없이 직접 수동 수정 후 "검수 완료" 처리
> ✅ **올바른 흐름**: "검수해줘" → qa.md Read → 프로토콜대로 전체 루프 실행 → 완료

**신설 배경**: 2026-05-20 "민화투 글 검수해줘" 요청 시 qa.md를 확인하지 않고 임의 수동 수정만 하고 완료 처리한 사고 이후 확정.

### 갭/문제 발견 시
- 시뮬레이션·리뷰에서 명백한 갭·모순 발견 시 묻지 말고 즉시 수정
- 큰 구조 변경(에이전트 통째 재설계·새 에이전트 추가·외부 도구 설치·환경 영구 변경)만 확인

### 에이전트 md 변경 시 (`.claude/agents/*.md`)
> **변경 실행 주체**: dev 에이전트. lead는 변경 내용 브리프 작성·오너 승인 확인·결과 검토만. lead 직접 편집 금지.

변경 작업 마무리 시점에 3단계 자동 실행:
1. 파일 상단 `**버전**` 줄 마이너 bump + 1줄 요약 (≤30자)
2. `C:\Claude_code\YYYY-MM-DD-agent\` 스냅샷 폴더 (같은 날 덮어쓰기)
3. `C:\Claude_code\agent_changelog.xlsx` 해당 탭 행 추가 (이력 누적)

### 세션 마무리 표준 (★ 2026-05-14 신설 / 2026-05-21 개정)

세션 마무리(핸드오프 갱신) 시점에 **반드시** "다음 세션 시작 멘트" 템플릿을 함께 제공한다. 새 세션은 이전 대화 컨텍스트가 0이므로, 이 멘트가 유일한 매끄러운 재개 경로다.

- **멘트 4요소**: ① 프로젝트 명시(`brain_health` / `C:\Claude_code`) ② 핸드오프 파일명 ③ **lead.md Read 명시** ④ 다음 할 일
- **표준 형식**: `"brain_health 세션이야. session_handoff_YYYY-MM-DD.md 읽고, lead.md 읽고, [할 일] 진행하자"`
- 세션 종료 보고 말미에 이 템플릿을 박스 또는 코드블록으로 제시 — 사용자가 복사·재사용 가능하도록
- 핸드오프 파일 자체에도 다음 세션 시작 멘트 템플릿을 포함시킨다.

> 🔴 **철칙 (★ 2026-05-21 확정)**: 매 세션 시작 시 `lead.md` Read는 핸드오프 파일 다음에 반드시 실행. 생략 시 팀장 실행 금지 규칙 인지 실패로 이어짐. lead.md를 읽지 않은 상태에서 어떤 실행 작업도 시작 불가.

---

## 📱 KakaoTalk 의무 발송 — 팀장 통합 알림 (★ 2026-05-19 의무화)

**🔴 선택 기능 아님 — 아래 두 상황에서 반드시 자동 전송**

**사용 도구**: `mcp__40dd940e-98f3-4c63-aba5-762cdc4aa158__KakaotalkChat-MemoChat`

### 트리거 1: 컨펌 요청 시 (사용자 결정 필요할 때)

lead가 사용자에게 방향 선택·승인을 요청해야 할 때 → 카톡 전송 후 대기.

```
🧠 [brain_health] 확인 요청
━━━━━━━━━━━━━━
❓ [결정이 필요한 내용 1~2줄]
선택지:
  A. [옵션 A]
  B. [옵션 B]
💬 Cowork에서 답변해 주세요
```

### 트리거 2: 세션 완료 시 (핸드오프 갱신 직후)

세션 마무리 핸드오프 갱신 완료 직후 → 카톡 전송 필수.

```
🧠 [brain_health] 세션 완료 (YYYY-MM-DD)
━━━━━━━━━━━━━━
✅ [완료 항목 1]
✅ [완료 항목 2]
✅ [완료 항목 3]
📋 다음: [다음 할 일]
📁 핸드오프: session_handoff_YYYY-MM-DD.md
```

> ❌ 생략 금지 — 사용자 요청 없어도 반드시 전송. 전송 실패 시 Cowork 응답에 실패 사유 명시.�