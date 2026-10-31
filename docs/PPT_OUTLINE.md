# PRESENTATION OUTLINE (PPT)

**PROJECT TITLE:** GitHub MCP Server: Connecting AI Assistants to Authenticated Developer Data  
**COURSE:** Master of Computer Applications (MCA) — Minor Project  
**INSTITUTION:** Vivekananda Institute of Professional Studies – Technical Campus (VIPS-TC), GGSIPU  
**STUDENT:** [Your Full Name] | **ENROLLMENT NO:** [Your Enrollment Number]  
**GUIDE:** [Guide Name]  

---

### Slide 1: Title Slide
- **Title:** GitHub MCP Server: Connecting AI Assistants to Authenticated Developer Data
- **Subtitle:** Minor Project Presentation — Master of Computer Applications (MCA)
- **Student Details:** [Your Name], Enrollment No: [Your Enrollment No]
- **Guide Details:** Under the guidance of [Guide Name]
- **Institution:** Department of Computer Applications, VIPS-TC, GGSIPU, Delhi

---

### Slide 2: Problem Statement & Motivation
- **The Core Problem:**
  - AI assistants (Claude, ChatGPT) are isolated from private developer environments behind authentication walls.
  - Queries like *"How many open issues across all my repos?"* or *"List stale issues in repo X"* cannot be answered by web search.
- **Why Existing Solutions Fall Short:**
  - Manual copy-pasting of terminal commands (`gh`) disrupts developer concentration.
  - Proprietary plugins lead to vendor lock-in and require sharing secrets with third-party cloud servers.
- **Project Motivation:**
  - Build a local, open-standard bridge connecting AI assistants directly to private GitHub data at zero financial cost.

---

### Slide 3: Project Objectives & Scope
- **Key Objectives:**
  - Implement a Python-based Model Context Protocol (MCP) server for GitHub.
  - Enforce a "Read-Only First" architectural philosophy (5 read tools).
  - Protect user data with a dry-run confirmation pattern on write operations (2 write tools).
  - Measure and optimize LLM tool selection reliability using a 50-question benchmark.
- **Strict Scope Boundaries:**
  - **In-Scope:** Repository metadata, issue inspection, cross-repo search aggregation, repo summaries, stale issue tracking, safe issue creation, and safe labeling.
  - **Out-of-Scope:** Destructive deletion operations (repositories, issues), code file search, and multi-tenant hosting.

---

### Slide 4: What is Model Context Protocol (MCP)?
- **Open Protocol:** Introduced by Anthropic in late 2024 as an open universal standard for AI tool calling.
- **Core Primitives:**
  - **Tools:** Executable routines the AI model can trigger.
  - **Resources:** Passive read-only data files or schemas.
  - **Prompts:** Reusable conversational templates.
- **Local stdio Transport:**
  - Client (Claude Desktop) and Server run as local sibling processes on the user's machine.
  - Communication flows over standard input/output (`stdin`/`stdout`) via JSON-RPC 2.0.
  - Credentials remain strictly local; zero cloud infrastructure needed.

---

### Slide 5: System Architecture & Data Flow
- **High-Level Interaction Diagram:**
  - `Claude Desktop (MCP Client)` ◄───(stdio / JSON-RPC)───► `MCP Server (server.py)`
  - `MCP Server` ───(Internal API Call)───► `GitHubClient (github_client.py)`
  - `GitHubClient` ───(HTTPS / Bearer Auth)───► `GitHub REST API (api.github.com)`
- **Key Separation of Concerns:**
  - `server.py`: Defines *what* tools exist (semantic interfaces, docstrings, bounds validation).
  - `github_client.py`: Handles *how* communication happens (HTTP requests, link pagination, rate limits).
  - `config.py`: Enforces startup credential checks via `.env`.

---

### Slide 6: Implemented MCP Tools
- **Read-Only Inspection Suite (5 Tools):**
  1. `list_repos`: Lists user repositories with stars, forks, visibility, and last updated timestamps.
  2. `list_open_issues`: Fetches open issues for a single repo; explicitly filters out Pull Requests.
  3. `count_open_issues_all`: Aggregates open issues across all user repositories in a single Search API call.
  4. `get_repo_summary`: Dashboard compiling description, stars, forks, recent commits, and open PRs.
  5. `stale_issues`: Detects inactive issues based on a customizable day threshold ($N$ days).
- **Protected Write Operations (2 Tools):**
  6. `create_issue`: Creates a new repository issue.
  7. `add_label`: Attaches labels to an existing issue.

---

### Slide 7: Security & Safety Guardrails
- **1. Dry-Run Confirmation Pattern:**
  - Write tools run in dry-run mode (`confirm=False`) by default, showing a preview without changing data.
  - Actual mutation executes only when `confirm=True` is explicitly passed after user review.
- **2. Principle of Least Privilege:**
  - Powered by fine-grained GitHub Personal Access Tokens (PAT).
  - Restricted strictly to `Issues (Read/Write)`, `Pull Requests (Read-Only)`, and `Metadata (Read-Only)`.
- **3. Protocol Stream Isolation:**
  - `sys.stdout` is reserved exclusively for MCP JSON-RPC protocol framing.
  - All operational logging is strictly redirected to `sys.stderr` to prevent JSON parsing crashes.

---

### Slide 8: Technical Implementation Highlights
- **Technology Stack:** Python 3.14, Python MCP SDK v2 (`MCPServer`), `httpx` (async-capable HTTP client), and `python-dotenv`.
- **RFC 5988 Pagination:**
  - Automatically parses `Link: rel="next"` HTTP headers to seamlessly paginate past GitHub's 100-item page limit.
- **Rate-Limit Defense:**
  - Inspects `X-RateLimit-Remaining` on every response.
  - Warns if quota falls below 10 calls; raises clean reset time notifications on exhaustion instead of crashing.
- **PR vs Issue Separation:**
  - Resolves GitHub API quirk where issues and PRs are returned together by filtering out items containing the `pull_request` key.

---

### Slide 9: Evaluation Methodology (50 Questions)
- **Experimental Setup:**
  - Curated 50 natural language test queries across 4 distinct categories.
  - Tested across English, Hindi, and Hinglish.
- **Query Categorization:**
  - **Direct Queries (20):** Explicit, unambiguous commands (e.g., *"Show my public repositories"*).
  - **Multilingual Queries (15):** Hindi & Hinglish prompts (e.g., *"Mere saare open issues dikhao"*).
  - **Ambiguous / Boundary Queries (8):** Prompts where multiple tools appear valid.
  - **Out-of-Scope Queries (7):** Prompts where no tool should trigger (e.g., *"Delete repository X"*).
- **Two-Round Optimization:**
  - **Round 1:** Baseline naive tool docstrings.
  - **Round 2:** Optimized docstrings with negative constraints and explicit scoping boundaries.

---

### Slide 10: Quantitative Results & Analysis
- **Benchmark Performance Table:**

| Metric | Round 1 (Baseline) | Round 2 (Optimized) | Improvement |
|---|---|---|---|
| **Overall Accuracy** | **90.0%** (45 / 50) | **98.0%** (49 / 50) | **+8.0%** |
| **Direct Queries** | 100.0% (20 / 20) | 100.0% (20 / 20) | 0.0% |
| **Multilingual (Hindi/Hinglish)** | 100.0% (15 / 15) | 100.0% (15 / 15) | 0.0% |
| **Ambiguous / Boundary Queries**| 62.5% (5 / 8) | **87.5%** (7 / 8) | **+25.0%** |
| **Out-of-Scope (No Tool)** | 71.4% (5 / 7) | **100.0%** (7 / 7) | **+28.6%** |

- **Key Takeaway:**
  - Multilingual queries achieved 100% accuracy because modern LLMs internally translate semantic intents prior to function dispatch.
  - Prompt disambiguation directly resolved keyword confusion between single-repo and account-wide counting.

---

### Slide 11: Live Demonstration Summary
- **Demonstration Flow:**
  - 1. **Discovery:** Claude Desktop initializes server and registers all 7 tools via stdio.
  - 2. **Cross-Repo Inquiry:** *"How many open issues do I have?"* triggers `count_open_issues_all` (returns account total: 5).
  - 3. **Deep Dive:** *"Show me the bug reports in Pranjay repo"* invokes `list_open_issues` with label filter.
  - 4. **Safety in Action:** *"Create an issue titled Fix CSS bug"* invokes `create_issue(confirm=False)` displaying a preview.
  - 5. **Confirmation:** User says *"Yes, go ahead"* -> `create_issue(confirm=True)` dispatches HTTP POST and returns live GitHub issue link.

---

### Slide 12: Conclusion & Future Scope
- **Conclusion:**
  - Built a fully operational, zero-cost, privacy-respecting MCP server connecting AI assistants to private GitHub developer data.
  - Demonstrated how semantic prompt engineering on tool descriptions eliminates tool selection errors (90% -> 98%).
  - Successfully adhered to least-privilege token access and dry-run safety principles.
- **Future Enhancements:**
  - Browser-based OAuth 2.0 authorization flow to replace manual PAT generation.
  - Local SQLite response caching with TTL to minimize rate limit consumption.
  - Pull request review and branch management support.
- **Thank You / Questions & Answers**
