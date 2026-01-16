param(
  [int]$Threads = 0,
  [int]$SizeMB = 256,
  [int]$Iters = 20
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $here
try {
  python .\run.py --threads $Threads --size-mb $SizeMB --iters $Iters
  Write-Host "OK: artifacts written to .\artifacts"
} finally {
  Pop-Location
}


