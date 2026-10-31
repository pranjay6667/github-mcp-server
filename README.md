# GitHub MCP Server

A Model Context Protocol (MCP) server connecting AI assistants to authenticated GitHub data — repositories, issues, pull requests, and stale-backlog detection — via the GitHub REST API.

**MCA Minor Project** · VIPS-TC, GGSIPU, Delhi

---

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                    LOCAL MACHINE                     │
│                                                      │
│  ┌──────────────┐    stdio (JSON-RPC)   ┌──────────┐ │
│  │  MCP Client  │ ◄══════════════════► │  server  │ │
│  │  (Inspector) │                      │   .py    │ │
│  └──────────────┘                      └────┬─────┘ │
│                                             │       │
│                                        HTTPS (REST) │
└─────────────────────────────────────────────┼───────┘
                                              ▼
                                     ┌─────────────────┐
                                     │ api.github.com  │
                                     └─────────────────┘
```

### Design Principles

| Principle | Implementation |
|---|---|
| Read-only first | 5 of 7 tools are strictly read-only |
| Safe writes | `create_issue` and `add_label` default to dry-run; require `confirm=True` |
| Least privilege | Fine-grained PAT scoped to Issues + PRs + Metadata |
| Protocol integrity | All logging → `stderr`; `stdout` reserved for MCP JSON-RPC |

---

## Tools

| # | Tool | Mode | Description |
|---|---|---|---|
| 1 | `list_repos` | Read | Authenticated user's repositories with stars, forks, visibility |
| 2 | `list_open_issues` | Read | Open issues for a repo; optional label filter; excludes PRs |
| 3 | `count_open_issues_all` | Read | Cross-repo open-issue count via GitHub Search API |
| 4 | `get_repo_summary` | Read | Dashboard: repo metrics + recent commits + open PRs |
| 5 | `stale_issues` | Read | Issues with no activity for N days |
| 6 | `create_issue` | Write | Creates issue after dry-run preview and explicit confirmation |
| 7 | `add_label` | Write | Adds labels to issue after dry-run preview and confirmation |

---

## Setup

### Prerequisites

- Python 3.10+
- A GitHub account with a fine-grained Personal Access Token

### Install

```bash
git clone https://github.com/pranjay6667/github-mcp-server.git
cd github-mcp-server

python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

pip install -r requirements.txt
```

### Configure Token

1. Create a fine-grained token at [github.com/settings/personal-access-tokens/new](https://github.com/settings/personal-access-tokens/new)
   - **Permissions**: Issues (Read & Write), Pull Requests (Read), Metadata (Read)
2. Copy `.env.example` → `.env` and paste your token:
   ```
   GITHUB_TOKEN=github_pat_...
   ```

---

## Usage

### MCP Inspector (recommended for testing)

```bash
mcp dev server.py
```

Opens a browser UI at `localhost:6274` with all 7 tools ready to invoke.

### Claude Desktop

Add to `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "github": {
      "command": "C:\\path\\to\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\server.py"]
    }
  }
}
```

Restart Claude Desktop. The tools icon will show 7 tools.

---

## Testing

```bash
python tests/test_tools.py       # All 7 tools against live API
python tests/test_safety.py      # Dry-run vs confirmed execution
python tests/test_protocol.py    # MCP JSON-RPC handshake
```

---

## Evaluation

A 50-question benchmark (`evaluation/questions.csv`) across English, Hindi, and Hinglish tests tool-routing accuracy:

| Round | Accuracy | Notes |
|---|---|---|
| Round 1 (naive prompts) | 90.0% (45/50) | Boundary ambiguity in cross-repo queries |
| Round 2 (refined prompts) | 98.0% (49/50) | Scope guards + negative constraints added |

Run the benchmark:

```bash
python evaluation/evaluate.py
```

---

## Project Structure

```
github-mcp-server/
├── server.py              # MCP server — 7 tool definitions
├── github_client.py       # GitHub REST API client
├── config.py              # Token loader from .env
├── requirements.txt
├── .env.example
├── tests/
│   ├── test_tools.py      # Tool integration tests
│   ├── test_safety.py     # Dry-run confirmation tests
│   └── test_protocol.py   # MCP handshake test
├── scripts/
│   └── seed_test_data.py  # Creates sample issues/labels
├── evaluation/
│   ├── questions.csv      # 50-question benchmark
│   ├── evaluate.py        # Benchmark runner
│   └── results.csv        # Round 1 & 2 results
└── docs/
    ├── PROJECT_REPORT.md
    ├── PPT_OUTLINE.md
    ├── DEMO_SCRIPT.md
    ├── VIVA_QUESTIONS.md
    └── INTERVIEW_PITCH.md
```

---

## Security

- **No hardcoded credentials** — token loaded from `.env` via `config.py`
- **`.env` in `.gitignore`** — never committed
- **Least privilege** — PAT scoped to metadata, issues, and PRs only
- **No destructive tools** — no deletion or repo-level mutation
- **Dry-run by default** — write tools preview before executing

---

## License

MIT
