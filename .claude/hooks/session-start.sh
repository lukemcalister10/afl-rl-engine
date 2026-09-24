#!/bin/bash
# SessionStart hook — Claude Code on the web only. Provisions the PINNED engine
# environment (setup_env.sh) and the absolute /home/claude/... layout
# (bootstrap.sh), and puts the pinned venv first on PATH for the session.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

REPO="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}"
VENV="${RL_VENV:-$HOME/rl_venv312}"

bash "$REPO/setup_env.sh"
bash "$REPO/bootstrap.sh"

# Two traps a fresh container sets, each of which used to cost a flight: the clone is shallow
# (two landing gates read history), and playwright-core is not resolvable from the repo's parent
# (the browser gates). Both best-effort: a failure here is reported by the gate that needs it.
if [ -f "$REPO/.git/shallow" ]; then
  git -C "$REPO" fetch --unshallow origin >/dev/null 2>&1 || echo "session-start hook: unshallow failed (gates needing history will say so)"
fi
PW_LINK="$(dirname "$REPO")/node_modules/playwright-core"
PW_SRC=/opt/node22/lib/node_modules/playwright/node_modules/playwright-core
if [ ! -e "$PW_LINK" ] && [ -d "$PW_SRC" ]; then
  mkdir -p "$(dirname "$PW_LINK")" && ln -s "$PW_SRC" "$PW_LINK"
fi

if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo "export RL_VENV=\"$VENV\"" >> "$CLAUDE_ENV_FILE"
  echo "export PATH=\"$VENV/bin:\$PATH\"" >> "$CLAUDE_ENV_FILE"
fi
echo "session-start hook: pinned env + bootstrap ready (venv=$VENV)"
