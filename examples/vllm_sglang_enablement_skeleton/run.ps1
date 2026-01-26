Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $here
try {
  python .\run.py
  Write-Host "OK: artifacts written to .\artifacts"
} finally {
  Pop-Location
}


