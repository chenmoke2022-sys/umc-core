Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot/..
try {
  # 1) audit
  pwsh .\scripts\audit_public.ps1

  # 2) share bundle
  pwsh .\scripts\make_share_bundle.ps1

  # 3) zip it
  $dist = ".\dist"
  New-Item -ItemType Directory -Force -Path $dist | Out-Null

  $ts = Get-Date -Format "yyyyMMdd-HHmmss"
  $zip = Join-Path $dist ("sw_public_release_" + $ts + ".zip")
  if (Test-Path $zip) { Remove-Item $zip -Force }

  Compress-Archive -Path ".\share_bundle\*" -DestinationPath $zip -Force
  Write-Host "OK: release zip generated: $zip"
} finally {
  Pop-Location
}


