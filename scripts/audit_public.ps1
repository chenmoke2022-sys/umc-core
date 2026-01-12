Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot/..
try {
  Write-Host "[1/4] validate artifacts"
  python .\tools\validate_artifacts.py --artifacts .\artifacts

  Write-Host "[2/4] verify manifest"
  python .\tools\verify_manifest.py --manifest .\artifacts\manifest.json

  Write-Host "[3/4] redaction scan (default: absolute paths)"
  python .\tools\scan_redaction.py --root .

  Write-Host "[4/4] forbidden weight/data scan"
  python .\tools\check_no_forbidden_files.py --root .

  Write-Host "OK: public audit passed"
} finally {
  Pop-Location
}


