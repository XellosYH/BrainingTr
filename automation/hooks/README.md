# brain_health Git Hooks

라운드테이블 2026-05-25 채택 룰 §3 — pre-commit hook 단계적 도입 (1단계).

## 파일

| 파일 | 용도 |
|---|---|
| `pre-commit` | 메인 hook 스크립트 (sh, Git for Windows 호환) |
| `install_hooks.ps1` | 새 환경에서 hook 재설치용 PowerShell 스크립트 |

## 6개 게이트 (1단계)

| # | 게이트 | 출처 에이전트 |
|---|---|---|
| 1 | BH_ prefix 검증 (widgets/post*_widget.html) | design_ui + game G1 |
| 2 | style 태그 단일행 검증 (wpautop 방어) | design_ui + game G3 |
| 3 | AudioContext 직접 호출 금지 (BH_getAC 경유) | sound |
| 4 | SVG 라이선스 마커 검증 | design |
| 5 | SVG NUL 패딩 검증 | design |
| 6 | 기획서 [검수 식별자] 검증 (staging 시) | game_planner |

## 설치

```powershell
powershell -ExecutionPolicy Bypass -File automation\hooks\install_hooks.ps1
```

## 우회 (긴급 시만)

```bash
git commit --no-verify -m "..."
```

> ⚠️ `--no-verify`는 사고 재발 위험. 게이트 FAIL 사유를 먼저 해결할 것.

## 화이트리스트 prefix (게이트 1)

- `BH_` — brain_health 정본 표준
- `wp-` — WordPress
- `swiper-`, `fa-`, `fas-`, `far-` — 라이브러리
- `gb-` — 자체 위젯
- `wk-`, `wk[대문자]` — post6 걷기 위젯 시스템 (`wk-wrap` 등 class + `wkItems` 등 camelCase id)

> post6는 `wk-` / `wk[A-Z]` 시스템 — 화이트리스트 등재 완료.

## 2단계 이후 계획

- sound gain 수치·BH_SoundMuted grep
- 이모지 검증 (WP wp_staticize_emoji 사고 방어)
- commit-msg hook 분리 (release/ prefix 시 별도 검증)
