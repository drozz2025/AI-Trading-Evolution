#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENDOR="$ROOT/vendor"
TARGET="$VENDOR/autoresearch-trading"

command -v git >/dev/null 2>&1 || { echo 'Git is required.'; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo 'Python 3 is required.'; exit 1; }

mkdir -p "$VENDOR"

if [ ! -d "$TARGET/.git" ]; then
  git clone https://github.com/dietmarwo/autoresearch-trading.git "$TARGET"
fi

cd "$TARGET"
git fetch --tags --force origin
git checkout main
git pull --ff-only origin main
python3 -m pip install --upgrade pip
python3 -m pip install -e .

echo 'AutoResearch laboratory installed under vendor/autoresearch-trading.'
echo 'Execution mode remains research/simulation only.'
