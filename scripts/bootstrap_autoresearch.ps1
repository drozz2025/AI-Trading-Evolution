$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$vendor = Join-Path $root 'vendor'
$target = Join-Path $vendor 'autoresearch-trading'

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'Git is required. Install Git for Windows first.'
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw 'Python is required. Install Python 3.11+ first.'
}

New-Item -ItemType Directory -Force -Path $vendor | Out-Null

if (-not (Test-Path (Join-Path $target '.git'))) {
    git clone https://github.com/dietmarwo/autoresearch-trading.git $target
}

Push-Location $target
try {
    git fetch --tags --force origin
    git checkout main
    git pull --ff-only origin main
    python -m pip install --upgrade pip
    python -m pip install -e .
}
finally {
    Pop-Location
}

Write-Host 'AutoResearch laboratory installed under vendor/autoresearch-trading.'
Write-Host 'Execution mode remains research/simulation only.'
