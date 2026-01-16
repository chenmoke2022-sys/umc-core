Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Push-Location $PSScriptRoot/../..
try {
  $art = ".\examples\quantization_llamacpp\artifacts"
  New-Item -ItemType Directory -Force -Path $art | Out-Null

  python .\tools\collect_env.py --out (Join-Path $art "env.json")

  # TODO: run the real benchmark here.
  # Requirements:
  # - Do NOT commit any weights into this repo.
  # - Do NOT write absolute paths into artifacts or docs.
  #
  # Example (pseudo):
  #   & .\third_party\llama.cpp\main.exe -m <path-to-public-gguf> -p "Hello" --timings
  #
  # Parse results and write results.json, then generate manifest:
  #   python .\tools\make_manifest.py --dir $art --out (Join-Path $art "manifest.json")
  #   python .\tools\verify_manifest.py --manifest (Join-Path $art "manifest.json")

  Write-Host "Edit this script to run the actual benchmark and write results.json"
  Write-Host "For a placeholder evidence pack, run: pwsh .\examples\quantization_llamacpp\make_demo_artifacts.ps1"
} finally {
  Pop-Location
}

