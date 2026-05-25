# brain_health pre-commit hook 재설치 스크립트
# 사용: 새 환경에서 git clone 후 또는 .git/hooks/ 삭제 시
# 실행: powershell -ExecutionPolicy Bypass -File automation\hooks\install_hooks.ps1

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$source = Join-Path $PSScriptRoot "pre-commit"
$target = Join-Path $repoRoot ".git\hooks\pre-commit"

if (-not (Test-Path $source)) {
    Write-Error "Source hook not found: $source"
    exit 1
}

if (-not (Test-Path (Split-Path $target))) {
    Write-Error ".git/hooks/ not found — not a git repo or .git missing"
    exit 1
}

Copy-Item -Path $source -Destination $target -Force
Write-Output "✅ pre-commit hook 설치 완료: $target"
Write-Output "    검증: bash .git/hooks/pre-commit"
Write-Output "    우회(권장 X): git commit --no-verify"
