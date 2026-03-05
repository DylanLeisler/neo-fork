#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROM_PATH="${SCRIPT_DIR}/PNEO.nds"

echo "Launching ROM: ${ROM_PATH}"
ls -l --time-style=long-iso "${ROM_PATH}"

../../noods.exe "${ROM_PATH}"
