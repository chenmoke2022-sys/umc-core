Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot/..
try {
  New-Item -ItemType Directory -Force -Path ".\artifacts" | Out-Null
  New-Item -ItemType Directory -Force -Path ".\_logs" | Out-Null

  Write-Host "[1/6] collect env.json"
  python .\tools\collect_env.py --out .\artifacts\env.json

  Write-Host "[2/6] seed results.json/report.md from templates (if missing)"
  if (-not (Test-Path ".\artifacts\results.json")) {
    Copy-Item ".\templates\results.json" ".\artifacts\results.json" -Force
  }
  if (-not (Test-Path ".\artifacts\report.md")) {
    Copy-Item ".\templates\report.md" ".\artifacts\report.md" -Force
  }

  Write-Host "[3/6] make manifest.json"
  python .\tools\make_manifest.py --dir .\artifacts --out .\artifacts\manifest.json

  Write-Host "[4/6] validate artifacts"
  python .\tools\validate_artifacts.py --artifacts .\artifacts

  Write-Host "[5/6] verify manifest"
  python .\tools\verify_manifest.py --manifest .\artifacts\manifest.json

  Write-Host "[6/6] redaction + forbidden file scan"
  python .\tools\scan_redaction.py --root .
  python .\tools\check_no_forbidden_files.py --root .

  Write-Host "OK: demo artifacts generated under .\artifacts\"
} finally {
  Pop-Location
}


