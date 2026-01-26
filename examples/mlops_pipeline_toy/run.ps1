Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot
try {
  $art = ".\\artifacts"
  New-Item -ItemType Directory -Force -Path $art | Out-Null

  python .\\run.py --out $art

  python ..\\..\\tools\\collect_env.py --out (Join-Path $art "env.json")
  python ..\\..\\tools\\make_manifest.py --dir $art --out (Join-Path $art "manifest.json")
  python ..\\..\\tools\\validate_artifacts.py --artifacts $art
  python ..\\..\\tools\\verify_manifest.py --manifest (Join-Path $art "manifest.json")

  Write-Host "OK: measured artifacts generated at $art"
} finally {
  Pop-Location
}


