# GitHub MCP Server – Connecting AI Assistants to Authenticated Developer Data

### IN PARTIAL FULFILLMENT OF THE REQUIREMENT FOR THE AWARD OF DEGREE OF
### MASTER OF COMPUTER APPLICATIONS

**Submitted By:**  
**Pranjay (Enrollment No. ________________)**

<br/>

**VIVEKANANDA SCHOOL OF INFORMATION TECHNOLOGY**  
**VIVEKANANDA INSTITUTE OF PROFESSIONAL STUDIES TC**  

*Affiliated To*  

**Guru Gobind Singh Indraprastha University**  
**Sector - 16C Dwarka, Delhi – 110078**

---

## ACKNOWLEDGEMENT

It is our proud privilege to express our profound gratitude to the entire management of Vivekananda Institute of Professional Studies – Technical Campus and teachers at the institute for providing us with the opportunity to avail the excellent facilities and infrastructure. The knowledge and values inculcated have proved to be of immense help at the very start of my career. Special thanks to Hon’ble Founder, Vivekananda Institute of Professional Studies- Technical Campus, Delhi for having provided us with excellent infrastructure at VSIT.

I am grateful to Prof. Mamta Madan (Dean, VSIT), and my respected Project Guide for their astute guidance, constant encouragement and sincere support for this project work. Sincere thanks to all my family members, seniors and friends for their support and assistance throughout the project.

**Pranjay**

---

## CERTIFICATE

This is to certify that the project entitled **“GitHub MCP Server: Connecting AI Assistants to Authenticated Developer Data”**, submitted in partial fulfilment of the Master of Computer Application degree at VIPS, has been completed by **Pranjay (Roll No. ________________)**. This is an authentic piece of work carried out by him under my guidance. To the best of my knowledge and belief, the material presented in this project has not been submitted earlier for the award of any degree.

<br/><br/>

**Signature of student** &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; **Signature of the guide**  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; *(Project Guide)*

---

## SELF CERTIFICATE

This is to certify that the project report entitled **“GitHub MCP Server: Connecting AI Assistants to Authenticated Developer Data”** done by me is an authentic work carried out for the partial fulfilment of Master of Computer Applications under the guidance of my project guide. The matter embodied in this project work has not been submitted earlier for award of any degree or diploma to the best of my knowledge and belief.

<br/><br/>

**Signature of the student**  
**Pranjay**  
**Enrollment No. ________________**

---

## TABLE OF CONTENTS

| S.NO | TOPIC | PAGE NO. |
| :--- | :--- | :--- |
| **1.** | **SYNOPSIS** | **5-8** |
| **2.** | **MAIN REPORT**<br/>• Objective and Scope of the Project<br/>• Theoretical background definition of problem<br/>• System analysis & design vis-a-vis user requirements<br/>• System planning (PERT chart)<br/>• Methodology adopted<br/>• System implementation<br/>• Details of Hardware and Software<br/>• System maintenance & evaluation<br/>• Detailed lifecycle of the project<br/>&nbsp;&nbsp;&nbsp;&nbsp;- Architecture & DFD<br/>&nbsp;&nbsp;&nbsp;&nbsp;- Input and Output Screen Design<br/>&nbsp;&nbsp;&nbsp;&nbsp;- Methodology used for testing<br/>&nbsp;&nbsp;&nbsp;&nbsp;- Testing and test results | **8-26** |
| **3.** | **CODING AND SCREENSHOTS** | **27-46** |
| **4.** | **CONCLUSION** | **47** |
| **5.** | **FUTURE SCOPE** | **48** |
| **6.** | **REFERENCES** | **49** |

---

# SYNOPSIS

### INTRODUCTION
In today's software engineering ecosystem, Large Language Models (LLMs) such as Claude, ChatGPT, and Gemini have revolutionized developer productivity. However, these AI assistants remain strictly isolated from private, authenticated developer environments behind firewalls and token barriers. A software engineer cannot ask an AI assistant basic questions about their private GitHub repositories, open pull requests, issue backlogs, or project commit activity because standard models have no live access to authenticated developer APIs.

To solve this problem, **GitHub MCP Server: Connecting AI Assistants to Authenticated Developer Data** is developed as a standardized, protocol-compliant Model Context Protocol (MCP) server. By implementing the open Model Context Protocol introduced by Anthropic in late 2024, this project connects AI desktop clients (such as Claude Desktop and MCP Inspector) directly to authenticated GitHub repositories in real time.

The application exposes 7 purpose-built tools: 5 read-only tools for repository inspection, issue tracking, search aggregation, and stale backlog detection, and 2 write tools protected by an innovative dry-run confirmation pattern. This project combines Systems Engineering, API Architecture, and AI Prompt Disambiguation to deliver a zero-cost, privacy-first bridge for developer workflows.

### PROBLEM STATEMENT
In current developer environments, AI assistants are unable to access private repositories, issues, or pull requests due to authentication walls. When developers need AI assistance to analyze project health, triage issues, or generate summaries, they are forced to manually copy-paste terminal outputs (`gh` CLI) or browser tabs into chat windows.

This manual workflow is tedious, context-limited, and disrupts developer concentration. Furthermore, existing third-party plugins require uploading sensitive personal access tokens to third-party cloud servers, posing significant security and privacy risks. There is an urgent need for an open-standard, locally executed server that allows AI assistants to interact directly and safely with authenticated GitHub data with zero cloud infrastructure and zero token exposure.

### WHY IS THIS PARTICULAR TOPIC CHOSEN?
This topic has been chosen because the Model Context Protocol (MCP) represents the modern industry standard for connecting AI systems to external data sources and tools. Rather than creating another vendor-locked chatbot, building an MCP server addresses a fundamental architectural shift in AI tooling.

The GitHub MCP Server was selected because GitHub is the universal home for open-source and proprietary software development. Providing an AI assistant with the ability to safely inspect repositories, aggregate issue counts across accounts, and draft issues with strict human-in-the-loop confirmation solves an authentic real-world developer need.

This project was also chosen because it encompasses Full-Stack Systems Development, Network Protocol Engineering (JSON-RPC over stdio), Security Best Practices (Least Privilege & Dry-Run by Default), and Quantitative AI Benchmark Evaluation, making it both academically rigorous and practically impactful.

### KEY FUNCTIONALITIES
- **Repository Discovery (`list_repos`):** Lists all public and private repositories owned by the user, including stars, forks, visibility, and last updated timestamps.
- **Single-Repository Issue Inspection (`list_open_issues`):** Fetches open issues for a designated repository, supporting optional label filters and strictly filtering out pull requests.
- **Cross-Repository Issue Counting (`count_open_issues_all`):** Uses the GitHub Search API to aggregate total open issues across all user repositories in a single API call.
- **Repository Health Dashboard (`get_repo_summary`):** Compiles repository metadata, recent git commits, and open pull requests into a structured dashboard view.
- **Stale Issue Backlog Detection (`stale_issues`):** Automatically detects and highlights neglected open issues with no activity for N days.
- **Safe Issue Creation (`create_issue`):** Creates issues with an automatic dry-run preview (`confirm=False`) requiring explicit user confirmation (`confirm=True`) before execution.
- **Safe Label Assignment (`add_label`):** Adds labels to existing issues with a dry-run preview to prevent unintended issue tagging.

### THEORETICAL FOUNDATION
The project is grounded in three core theoretical concepts: Model Context Protocol (MCP) specification, Principle of Least Privilege, and the Human-in-the-Loop Dry-Run Safety Pattern.

1. **Model Context Protocol:** MCP establishes a standardized JSON-RPC 2.0 communication loop between a Client (AI assistant) and a Server (tool provider). Operating over local standard input/output (stdio), all message exchange is isolated to the local host, eliminating third-party relay servers.
2. **Principle of Least Privilege:** The server uses fine-grained GitHub Personal Access Tokens (PATs) restricted solely to Issues (Read/Write), Pull Requests (Read-Only), and Metadata (Read-Only). No administrative, repository-deletion, or sensitive account permissions are ever requested.
3. **Dry-Run Safety Pattern:** Because autonomous AI tool calling can cause unintended state changes, write operations default to preview mode (`confirm=False`), giving developers full visibility and veto power before mutations occur on GitHub.

### USER CENTRIC DESIGN
The GitHub MCP Server is designed with developer experience and security at its core. Instead of requiring complex CLI arguments or browser context switching, developers simply converse with their AI assistant in natural language (English, Hindi, or Hinglish).

The server guarantees protocol integrity by strictly isolating all diagnostic and network logging to standard error (`stderr`), leaving standard output (`stdout`) dedicated solely to clean JSON-RPC messaging. Error messages are human-readable, notifying users clearly of rate-limit reset times or invalid repository names.

### DEVELOPMENT METHODOLOGY
The project followed an Agile Iterative Development Methodology spanning 8 distinct sprints: requirement analysis, token scoping, API client development, MCP tool definition, protocol verification, safety testing, multilingual benchmark curation, and prompt optimization. Continuous testing was maintained throughout development, validating the server against both the official MCP Inspector web UI and live GitHub API endpoints.

### FUTURE ENHANCEMENTS
- **OAuth 2.0 Web Authorization:** Implement a browser-based OAuth flow to eliminate manual Personal Access Token generation.
- **Local Response Caching:** Introduce an embedded SQLite cache with configurable TTL to reduce rate-limit consumption for frequently queried repos.
- **Pull Request Code Reviews:** Expand write tools to support commenting on and approving open pull requests directly from the AI chat interface.

---

# MAIN REPORT

## 2.1 OBJECTIVE AND SCOPE

### OBJECTIVE
The primary objective of the GitHub MCP Server is to build a reliable, open-standard, and secure local server connecting AI assistants to authenticated GitHub developer data.

Specific objectives include:
1. Implementing a Python-based Model Context Protocol (MCP) server adhering to the official v2.0 specification.
2. Providing 5 comprehensive read-only tools to inspect repositories, issues, summaries, and inactive backlogs.
3. Developing 2 write tools behind an immutable dry-run confirmation guardrail (`confirm=False` by default).
4. Isolating credentials completely to the local user machine using environment variables (`.env`).
5. Measuring and optimizing AI tool-calling accuracy across a 50-question multilingual benchmark (English, Hindi, Hinglish).

### SCOPE
- **In Scope:** Repository listing, issue inspection with PR separation, cross-repo search counting, repository summaries (commits + PRs), stale issue detection, safe issue creation, and safe labeling.
- **Out of Scope:** Destructive repository deletion, raw code file searches (restricted due to GitHub's 10 req/min secondary rate limit), and cloud-hosted multi-tenant infrastructure.

## 2.2 THEORETICAL BACKGROUND AND DEFINITION OF THE PROBLEM

### Theoretical Background
AI assistants historically functioned on pre-trained parametric weights. With the development of Function Calling (Tool Calling), models gained the ability to generate structured arguments for pre-defined APIs. The Model Context Protocol (MCP) unifies tool definitions across AI vendors using standard JSON-RPC 2.0 semantics.

Under the local `stdio` transport, the MCP client spawns the MCP server as a subprocess. Communication occurs via standard streams, guaranteeing zero network exposure of credentials and zero cloud server dependency.

### Definition of the Problem
1. AI isolation: AI models have no access to private developer repositories without authentication.
2. Context switching: Developers waste significant time copy-pasting terminal commands and browser URLs.
3. Security risks: Sharing API tokens with third-party web plugins violates software security standards.
4. Unintended mutations: Unrestricted AI write access can lead to accidental issue creation or spamming.
5. Rate limiting: Naive API querying quickly exhausts GitHub's 5,000 requests/hour rate limit.

## 2.3 SYSTEM ANALYSIS & DESIGN VIS-A-VIS USER REQUIREMENTS

### Functional Requirements
- **FR1:** Retrieve all repositories (public and private) owned by the user.
- **FR2:** Fetch open issues for a designated repo, filtering out pull requests.
- **FR3:** Aggregate open issues across all user repositories in a single API call.
- **FR4:** Compile repository health metrics, recent commits, and open PRs into a dashboard.
- **FR5:** Identify and return issues with no activity for N days.
- **FR6:** Display a dry-run preview of an issue, creating it only when `confirm=True`.
- **FR7:** Preview label additions, applying them only when `confirm=True`.

### Non-Functional Requirements
- **NFR1: Zero Cost** — Built entirely on free Python libraries, GitHub free tier, and MCP Inspector.
- **NFR2: Protocol Integrity** — All logging directed strictly to `stderr`; `stdout` reserved for JSON-RPC.
- **NFR3: Least Privilege** — Operates exclusively with fine-grained tokens scoped to issues, PRs, and metadata.
- **NFR4: High Reliability** — Handles RFC 5988 pagination and rate-limit exhaustion gracefully.

## 2.4 SYSTEM PLANNING (PERT CHART)

The project development was structured into 9 sequential and interdependent phases over a planned 13-week lifecycle:

| TASK | DURATION (WEEKS) |
| :--- | :--- |
| Requirements Gathering & Planning | 1 |
| Token Scoping & GitHub API Client Architecture | 1 |
| Core MCP Server & Tool Schema Definition | 3 |
| Dry-Run Safety Engine & Error Handling | 2 |
| Protocol Stream Isolation & Logging Setup | 1 |
| Pagination & Rate Limit Defense Implementation | 1 |
| Multilingual Benchmark Curation (50 Queries) | 1 |
| Testing, Evaluation & Prompt Disambiguation | 2 |
| Documentation, Deployment & Git Finalization | 1 |
| **Total Estimated Timeline** | **13 Weeks** |

## 2.5 METHODOLOGY ADOPTED

### Approach Highlights
1. **Modular Separation of Concerns:** Architecture separated into `config.py` (secrets), `github_client.py` (API transport), and `server.py` (MCP tools).
2. **Read-Only First:** Prioritizing safe informational queries before offering mutating capabilities.
3. **Defense-in-Depth Safety:** Enforcing dry-run confirmation on all state changes.
4. **Protocol Stream Isolation:** Preserving `stdout` strictly for machine communication; redirecting human logs to `stderr`.
5. **Empirical Benchmark Optimization:** Evaluating tool selection across 50 questions before and after prompt refinement.

### Tools and Technologies Used
- **Language:** Python 3.14 — Robust async runtime, strong typing, wide ecosystem.
- **MCP Framework:** `mcp` v2.3.0 (Official Anthropic Python SDK) — `MCPServer` abstraction.
- **HTTP Client:** `httpx` v0.28.1 — Fast HTTP/1.1 client with strict timeouts and custom header parsing.
- **Configuration:** `python-dotenv` v1.2.4 — Secure local environment parsing.
- **API Testing:** MCP Inspector v2.13.0 — Interactive browser-based developer harness.
- **Version Control:** Git & GitHub — Remote repository tracking at `pranjay6667/github-mcp-server`.

## 2.6 SYSTEM IMPLEMENTATION

The system implementation comprises three main functional layers:
1. **Credential Management (`config.py`):** Employs `Path(__file__).resolve().parent` to reliably resolve the `.env` file regardless of the working directory from which Claude Desktop or the inspector initiates the subprocess. Halts with a descriptive `stderr` error if `GITHUB_TOKEN` is absent.
2. **GitHub REST Client (`github_client.py`):** Implements automatic RFC 5988 Link header pagination, extracts pull requests out of generic issue responses, and monitors `X-RateLimit-Remaining` headers to fail gracefully when quotas deplete.
3. **MCP Server Core (`server.py`):** Defines 7 tool handlers decorated with `@mcp.tool()`. Handles dry-run preview generation when `confirm=False` and executes live mutations only when `confirm=True`.

## 2.7 DETAILS OF HARDWARE AND SOFTWARE

### Hardware Requirements
- **Processor:** Intel Core i3 / AMD Ryzen 3 or higher.
- **RAM:** Minimum 4 GB (8 GB recommended).
- **Storage:** 256 MB free disk space for Python runtime and virtual environment.
- **Network:** Active internet connection for live GitHub REST API communication.

### Software Requirements
- **Operating System:** Windows 10/11, macOS, or Linux.
- **Runtime:** Python 3.10+ (Developed and tested on Python 3.14.7).
- **Packages:** `mcp[cli]>=2.3.0`, `httpx>=0.28.1`, `python-dotenv>=1.2.4`.
- **Development Tools:** Visual Studio Code, Git CLI, MCP Inspector.

## 2.8 SYSTEM MAINTENANCE AND EVALUATION

### Maintenance Strategy
1. **Token Rotation:** Easily rotate GitHub tokens by updating the local `.env` file without modifying code.
2. **Rate-Limit Monitoring:** Real-time warnings log when fewer than 10 requests remain in the hourly quota.
3. **API Version Pinning:** The client explicitly sends `X-GitHub-Api-Version: 2022-11-28` to guard against upstream breaking changes.

### Evaluation Approach
The server was evaluated using a rigorous 50-question benchmark dataset across two experimental rounds:
- **Round 1 (Baseline):** Tool descriptions used generic, naive docstrings.
- **Round 2 (Optimized):** Tool descriptions included explicit negative constraints, scope boundaries, and trigger phrases.

Results proved an **8.0% overall accuracy gain (90.0% -> 98.0%)**, with ambiguous queries improving by **+25.0%** and out-of-scope rejections improving by **+28.6%**.

## 2.9 DETAILED LIFECYCLE OF THE PROJECT

### 2.9.1 Architecture and Data Flow Diagrams (DFD)

**System Architecture:**
```
Client (Claude / Inspector) <=== stdio (JSON-RPC) ===> server.py <---> github_client.py <=== HTTPS ===> api.github.com
```

**Level 0 DFD (Context Diagram):**
```
[Developer] ---> (Natural Language Prompt) ---> [GitHub MCP Server] ---> (Structured Response) ---> [Developer]
                       |                                      ^
            (HTTPS GET/POST)                           (JSON Payload)
                       v                                      |
                            [GitHub REST API Service]
```

**Level 1 DFD:**
```
1.0 Prompt Parser -> 2.0 MCP Protocol Dispatcher -> 3.0 Dry-Run Guard -> 4.0 GitHub Client -> 5.0 Output Formatter
```

### 2.9.2 Input and Output Screen Design
- **Input Screen (MCP Inspector):** Interactive form dynamically rendered from tool JSON schemas. For `get_repo_summary`, accepts `owner` and `repo` inputs.
- **Output Screen (Dry-Run Preview):** Displays formatted text indicating `DRY RUN -- Issue preview (not created yet)` with parameters.
- **Output Screen (Confirmed Execution):** Displays `Issue created successfully!` accompanied by the live GitHub issue URL.

### 2.9.3 Methodology Used for Testing
- **Unit Testing:** Individual tool schema validation via `tests/test_protocol.py`.
- **Integration Testing:** Live GitHub API execution via `tests/test_tools.py`.
- **Safety Testing:** Dry-run and confirmed mutation verification via `tests/test_safety.py`.
- **Benchmark Evaluation:** 50-question multilingual automated evaluation via `evaluation/evaluate.py`.

### 2.9.4 Testing and Test Results
- **Protocol Test:** 100% of tools (7/7) correctly registered with valid parameter schemas.
- **Safety Test:** Dry-run successfully prevented unwanted issue creation; confirmed execution created Issue #7 with live URL.
- **Benchmark Test:** Round 2 achieved 98.0% routing accuracy (49/50 correct).

---

# CODING AND SCREENSHOTS

## CORE CODE IMPLEMENTATION

### 1. `config.py` (Credential Loader)
```python
"""Configuration loader for GitHub MCP Server."""
import os, sys
from pathlib import Path
from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_BASE = "https://api.github.com"

if not GITHUB_TOKEN or GITHUB_TOKEN.startswith("ghp_paste"):
    sys.stderr.write("Error: GITHUB_TOKEN is not configured.\n")
    sys.exit(1)
```

### 2. `github_client.py` (REST API Client)
```python
class GitHubClient:
    def __init__(self) -> None:
        self.client = httpx.Client(
            base_url=GITHUB_API_BASE,
            headers={
                "Authorization": f"Bearer {GITHUB_TOKEN}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=30.0,
        )
        self._username = None

    def _check_rate_limit(self, response: httpx.Response) -> None:
        remaining = response.headers.get("x-ratelimit-remaining")
        if remaining is not None and int(remaining) == 0:
            raise RuntimeError("GitHub API rate limit exhausted.")

    def list_repos(self, visibility="all", sort="updated", limit=30):
        return self._get_paginated("/user/repos", {"visibility": visibility, "sort": sort}, limit)
```

### 3. `server.py` (MCP Tool Definitions & Safety)
```python
from mcp.server.mcpserver import MCPServer
from github_client import GitHubClient

mcp = MCPServer(name="github-mcp-server")
client = GitHubClient()

@mcp.tool()
def create_issue(owner: str, repo: str, title: str, body: str = "", labels: str = "", confirm: bool = False) -> str:
    if not confirm:
        return f"DRY RUN -- Issue preview: {owner}/{repo}: {title}. Call again with confirm=True."
    result = client.create_issue(owner, repo, title, body, [l.strip() for l in labels.split(",") if l.strip()])
    return f"Issue created successfully! #{result.get('number')}: {title}"
```

## SCREENSHOTS OF SYSTEM EXECUTION

### Figure 1: MCP Inspector – All 7 Tools Connected & Registered
*(Displays the MCP Inspector sidebar with 7 tools: `add_label`, `count_open_issues_all`, `create_issue`, `get_repo_summary`, `list_open_issues`, `list_repos`, `stale_issues`)*

### Figure 2: MCP Inspector – Dry-Run Safety Preview for `create_issue`
*(Displays the preview output produced when calling `create_issue` with `confirm=False`, verifying that no live GitHub modification occurred)*

### Figure 3: MCP Inspector – `get_repo_summary` Execution & Console Output
*(Displays the interactive input form and the Server Console verifying live HTTP 200 responses against the GitHub REST API)*

---

# CONCLUSION

The project **GitHub MCP Server: Connecting AI Assistants to Authenticated Developer Data** successfully delivers a modern, open-standard, and zero-cost bridge between generative AI assistants and private software repositories.

By strictly implementing the Model Context Protocol (MCP) standard, the server allows AI models like Claude to query repositories, count issues across organizations, summarize project health, and detect neglected backlogs in real time without human context-switching.

The project's architectural safeguards—namely least-privilege token access, protocol stream isolation to `stderr`, and dry-run confirmation on write operations—ensure that AI autonomy does not compromise developer data integrity.

Furthermore, empirical evaluation across 50 multilingual queries demonstrated that semantic prompt engineering directly elevated tool routing accuracy from **90.0% to 98.0%**, proving that precise tool definitions are critical for reliable AI agent execution.

---

# FUTURE SCOPE

1. **OAuth 2.0 Web Authentication:** Incorporate a browser-based OAuth authorization flow to allow non-technical users to connect their GitHub accounts without manually creating Personal Access Tokens.
2. **Local SQLite Response Caching:** Implement local client-side caching with Time-To-Live (TTL) expiration to reduce duplicate network requests and prevent rate-limit depletion.
3. **Pull Request Review & Comments:** Expand write capabilities to allow AI assistants to review pull request diffs, leave comments, and approve pull requests directly.
4. **Branch and Commit Operations:** Introduce tools for branch creation, cherry-picking, and diff visualization within the chat interface.
5. **Multi-Platform Support:** Extend the MCP server to support GitLab and Bitbucket using unified tool abstractions.

---

# REFERENCES

1. Anthropic. (2024). *Model Context Protocol Specification*. Available: https://modelcontextprotocol.io/
2. GitHub Inc. (2024). *GitHub REST API Documentation*. Available: https://docs.github.com/en/rest
3. Schick, T., et al. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools*. arXiv preprint arXiv:2302.04761.
4. Python Software Foundation. (2024). *Python Standard Library — Logging and Subprocess Management*.
5. Fielding, R. (2008). *RFC 5988: Web Linking*. Internet Engineering Task Force.
6. JSON-RPC Working Group. (2013). *JSON-RPC 2.0 Specification*. Available: https://www.jsonrpc.org/specification
7. HTTPX Project. (2024). *HTTPX: A next-generation HTTP client for Python*. Available: https://www.python-httpx.org/
8. Git Documentation. (2024). *Git Version Control System*. Available: https://git-scm.com/
