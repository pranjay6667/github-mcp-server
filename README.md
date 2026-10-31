# GitHub MCP Server

A Model Context Protocol (MCP) server written in Python connecting AI assistants (such as Claude Desktop) to authenticated GitHub repositories and issues.

Developed as an MCA Minor Project at **Vivekananda Institute of Professional Studies – Technical Campus (VIPS-TC), GGSIPU, Delhi**.

---

## 📌 Architecture & Design Principles

```
┌────────────────────────────────────────────────────────┐
│                      LOCAL MACHINE                     │
│                                                        │
│  ┌─────────────────┐      stdio       ┌──────────────┐ │
│  │   MCP Client    │ ◄══════════════► │  MCP Server  │ │
│  │ (Claude Desktop)│    JSON-RPC      │ (server.py)  │ │
│  └─────────────────┘                  └──────┬───────┘ │
│                                              │         │
│                                          HTTP requests │
│                                              │         │
└──────────────────────────────────────────────┼─────────┘
                                               ▼
                                      ┌──────────────────┐
                                      │  GitHub REST API │
                                      │ (api.github.com) │
                                      └──────────────────┘
```

- **Read-Only First**: Five read-only tools allow safe repository data inspection.
- **Safety by Default**: Write operations (`create_issue`, `add_label`) run in **dry-run** mode (`confirm=False`) by default. They generate a preview and require explicit confirmation (`confirm=True`) before executing.
- **Least Privilege**: Operates via fine-grained Personal Access Tokens scoped strictly to Issues and Pull Requests.
- **Protocol Integrity**: All logging is routed to `sys.stderr` so that `sys.stdout` remains dedicated exclusively to MCP stdio JSON-RPC messages.

---

## 🛠️ Tools Overview

| Tool | Category | Safety / Mode | Description |
|---|---|---|---|
| `list_repos` | Read-only | Safe | Lists repositories owned by the authenticated user with stars, forks, visibility, and last updated time. |
| `list_open_issues` | Read-only | Safe | Lists open issues for a specific repo (filters out pull requests). Supports label filtering. |
| `count_open_issues_all` | Read-only | Safe | Uses GitHub Search API to count open issues across all user repositories in a single API call. |
| `get_repo_summary` | Read-only | Safe | Fetches repository details, recent commits, and open pull requests in a structured dashboard view. |
| `stale_issues` | Read-only | Safe | Finds open issues with no comments or updates for $N$ days (sorted ascending to optimize API usage). |
| `create_issue` | Write | **Dry-run by default** | Creates an issue only when `confirm=True`. Otherwise returns a preview. |
| `add_label` | Write | **Dry-run by default** | Adds labels to an issue only when `confirm=True`. Otherwise returns a preview. |

---

## 🚀 Setup & Installation

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.14)
- A GitHub Account
- Claude Desktop or MCP Inspector

### 2. Clone & Create Virtual Environment
```powershell
git clone <your-repo-url>
cd github-mcp-server

python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS / Linux
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure GitHub Token
1. Generate a fine-grained token at [GitHub Token Settings](https://github.com/settings/personal-access-tokens/new):
   - **Repository access**: All repositories (or select specific repositories)
   - **Permissions**:
     - *Issues*: Read and Write
     - *Pull requests*: Read-only
     - *Metadata*: Read-only (default)
2. Copy `.env.example` to `.env`:
   ```powershell
   copy .env.example .env
   ```
3. Open `.env` and set your token:
   ```env
   GITHUB_TOKEN=github_pat_your_token_here
   ```

---

## 🧪 Testing

### Test with the MCP Inspector
Run the official MCP Inspector to interact with your tools in a browser UI:
```powershell
mcp dev server.py
```

### Run Automated Unit / Safety Verification
```powershell
python test_all_tools.py
python test_safety_quality.py
```

---

## 🖥️ Connecting to Claude Desktop

Add the server to your Claude Desktop configuration file:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

Add the following under `mcpServers`:

```json
{
  "mcpServers": {
    "github": {
      "command": "C:\\Users\\pranj\\.gemini\\antigravity\\scratch\\github-mcp-server\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\pranj\\.gemini\\antigravity\\scratch\\github-mcp-server\\server.py"
      ]
    }
  }
}
```

Restart Claude Desktop. The hammer icon (tools) will show all 7 tools ready to use.

---

## 🔒 Security Checklist

- [x] **No Hardcoded Credentials**: Tokens loaded exclusively via `config.py` from `.env`.
- [x] **Git Hygiene**: `.env` and `.venv/` strictly included in `.gitignore`.
- [x] **Least Privilege**: Fine-grained token scoped only to metadata, issues, and PRs.
- [x] **No Destructive Capabilities**: Server intentionally provides no issue deletion or repo deletion tools.
- [x] **State-Change Guardrail**: All write tools enforce preview confirmation prior to mutating live data.
- [x] **Rate Limit Guard**: Monitors `X-RateLimit-Remaining` to fail gracefully instead of crashing.
