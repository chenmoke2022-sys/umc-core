Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot/..
try {
  $outDir = ".\share_bundle"
  if (Test-Path $outDir) { Remove-Item $outDir -Recurse -Force }
  New-Item -ItemType Directory -Force -Path $outDir | Out-Null

  Copy-Item ".\README.md" $outDir -Force
  Copy-Item ".\AUDIT.md" $outDir -Force
  Copy-Item ".\REPRODUCE.md" $outDir -Force
  Copy-Item ".\SECURITY.md" $outDir -Force

  New-Item -ItemType Directory -Force -Path "$outDir\artifacts" | Out-Null
  Copy-Item ".\artifacts\*" "$outDir\artifacts\" -Force

  New-Item -ItemType Directory -Force -Path "$outDir\docs" | Out-Null
  Copy-Item ".\docs\RELEASE_CHECKLIST.md" "$outDir\docs\" -Force
  Copy-Item ".\docs\SPEECH_BLACKLIST.md" "$outDir\docs\" -Force
  Copy-Item ".\docs\SHARE_WITH_RECRUITER.md" "$outDir\docs\" -Force

  Write-Host "OK: share bundle generated at $outDir (do not include any weights/data)"
} finally {
  Pop-Location
}


