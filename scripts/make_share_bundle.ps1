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

          # assets referenced by README
          New-Item -ItemType Directory -Force -Path "$outDir\assets" | Out-Null
          Copy-Item ".\assets\benchmark_card.svg" "$outDir\assets\" -Force

  New-Item -ItemType Directory -Force -Path "$outDir\artifacts" | Out-Null
  Copy-Item ".\artifacts\*" "$outDir\artifacts\" -Force

  Write-Host "OK: share bundle generated at $outDir (do not include any weights/data)"
} finally {
  Pop-Location
}


