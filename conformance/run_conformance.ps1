Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot/..
try {
  $outDir = ".\conformance"
  New-Item -ItemType Directory -Force -Path $outDir | Out-Null

  $result = [ordered]@{
    schema_version = "0.1"
    timestamp_utc = (Get-Date).ToUniversalTime().ToString("o")
    checks = @()
    passed = $true
  }

  function Add-Check($name, $ok, $details) {
    $result.checks += [ordered]@{ name = $name; ok = [bool]$ok; details = $details }
    if (-not $ok) { $result.passed = $false }
  }

  try {
    pwsh .\scripts\audit_public.ps1 | Out-Null
    Add-Check "audit_public" $true "audit_public.ps1 passed"
  } catch {
    Add-Check "audit_public" $false $_.Exception.Message
  }

  # Check required public docs exist (contract)
  $requiredDocs = @(
    ".\docs\RELEASE_CHECKLIST.md",
    ".\docs\SPEECH_BLACKLIST.md",
    ".\docs\BRANCHING_AND_RELEASE_POLICY.md",
    ".\docs\OSS_COMPLIANCE.md",
    ".\docs\LTS_AND_ROLLBACK_POLICY.md",
    ".\docs\CERTIFICATION.md",
    ".\REPRODUCE.md",
    ".\AUDIT.md",
    ".\SECURITY.md",
    ".\LICENSE",
    ".\NOTICE"
  )
  $missing = @()
  foreach ($p in $requiredDocs) { if (-not (Test-Path $p)) { $missing += $p } }
  if ($missing.Count -eq 0) {
    Add-Check "required_docs" $true "all required docs present"
  } else {
    Add-Check "required_docs" $false ("missing: " + ($missing -join ", "))
  }

  $outJson = Join-Path $outDir "conformance_result.json"
  ($result | ConvertTo-Json -Depth 6) | Out-File -FilePath $outJson -Encoding UTF8

  if ($result.passed) {
    Write-Host "OK: conformance passed. Wrote $outJson"
    exit 0
  }
  Write-Host "FAILED: conformance failed. See $outJson"
  exit 2
} finally {
  Pop-Location
}


