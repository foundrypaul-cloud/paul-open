#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if ! command -v agy >/dev/null 2>&1; then
  echo "Installing Google Antigravity CLI..."
  curl -fsSL https://antigravity.google/cli/install.sh | bash
fi

if ! command -v agy >/dev/null 2>&1; then
  echo "Antigravity CLI was installed but 'agy' is not yet on PATH."
  echo "Open a new terminal, then run: agy --version"
  exit 1
fi

echo "Antigravity CLI: $(agy --version)"

python - <<'PY'
import json
from pathlib import Path

config = Path('.agents/mcp_config.json')
data = json.loads(config.read_text())
kaggle = data.get('mcpServers', {}).get('kaggle', {})
if kaggle.get('serverUrl') != 'https://www.kaggle.com/mcp':
    raise SystemExit('Kaggle MCP configuration is missing or invalid')
print('Kaggle MCP workspace configuration: OK')
PY

cat <<'EOF'

PAUL Open is ready for Antigravity.

Next:
  1. Run: agy
  2. In Antigravity, open /mcp and confirm the "kaggle" server is visible.
  3. Authorize Kaggle via OAuth when prompted. If OAuth discovery is unavailable,
     invoke Kaggle's MCP "authorize" tool from the agent.

Optional classic Kaggle API authentication:
  - Put KAGGLE_API_TOKEN=KGAT_... in your local .env only.
  - Never commit the token or kaggle.json.
EOF
