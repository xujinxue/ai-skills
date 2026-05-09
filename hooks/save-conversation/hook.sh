#!/usr/bin/env bash
set -euo pipefail

# hook.sh 所在目录
HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 当前工作目录
WORKSPACE_DIR="$(pwd)"

mkdir -p "$WORKSPACE_DIR/log"

conda run --no-capture-output -n torch_py310 python \
  "$HOOK_DIR/scripts/save_conversation.py" \
  --out-dir "$WORKSPACE_DIR/log"
