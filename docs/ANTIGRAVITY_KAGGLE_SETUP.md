# Antigravity + Kaggle setup for PAUL Open

PAUL Open supports Google Antigravity IDE/CLI as a repository-scoped agent environment and Kaggle through the official remote MCP server.

## Repository integration

The workspace MCP configuration is committed at:

```text
.agents/mcp_config.json
```

It registers:

```text
https://www.kaggle.com/mcp
```

Antigravity 2.0, Antigravity IDE, and Antigravity CLI can discover workspace MCP configuration from `.agents/mcp_config.json`.

## First-time local setup

From the repository root on macOS or Linux:

```bash
bash scripts/setup_antigravity_kaggle.sh
```

The script installs Google Antigravity CLI when `agy` is not already available and validates the repository's Kaggle MCP configuration.

Then launch:

```bash
agy
```

Open `/mcp` inside Antigravity and confirm that `kaggle` is present. Complete Kaggle OAuth authorization when prompted. If the client does not initiate OAuth discovery automatically, ask the agent to invoke Kaggle's MCP `authorize` tool.

## Antigravity IDE

Open the cloned `paul-open` repository as the workspace. The repository-local `.agents/mcp_config.json` is shared with the CLI. In the Agent panel, open **MCP Servers** to verify or reload the Kaggle connection.

## Optional KGAT token fallback

The preferred Antigravity path is OAuth through Kaggle MCP. For classic Kaggle API or CLI calls, a Kaggle token can be stored locally as:

```bash
KAGGLE_API_TOKEN=KGAT_...
```

Put it in `.env`, never in `.env.example`, `.agents/mcp_config.json`, a notebook, a shell script, or Git history.

The repository ignores `.env`, `kaggle.json`, `.kaggle/`, credential JSON files, and common secret files.

## GitHub workflow

Antigravity operates on the normal local Git clone. Use the existing Git remote for `foundrypaul-cloud/paul-open`; there is no separate "Antigravity GitHub connector" required for local repository editing. Authentication for pushing/pulling remains your normal Git/GitHub credential flow.

## DPO V2 / Kaggle workflow

After Kaggle authorization, use Antigravity to inspect and modify the repository locally, then use the Kaggle MCP/API surface for Kaggle-side resources. Keep the current DPO V2 experiment methodology and repository configuration as the source of truth; do not place private adapters, generated checkpoints, Kaggle tokens, or other secrets in Git.
