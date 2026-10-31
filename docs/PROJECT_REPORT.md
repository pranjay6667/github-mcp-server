# PROJECT REPORT

**TITLE:** GitHub MCP Server: Connecting AI Assistants to Authenticated Developer Data  
**COURSE:** Master of Computer Applications (MCA) — Minor Project  
**INSTITUTION:** Vivekananda Institute of Professional Studies – Technical Campus (VIPS-TC), GGSIPU, Delhi  
**STUDENT:** [Your Full Name]  
**ENROLLMENT NO.:** [Your Enrollment Number]  
**PROJECT GUIDE:** [Guide Name]  
**ACADEMIC YEAR:** 2026–2027  

---

## TABLE OF CONTENTS

1. **Chapter 1: Introduction**
   - 1.1 Problem Statement
   - 1.2 Motivation
   - 1.3 Project Objectives
   - 1.4 Scope and Boundaries
2. **Chapter 2: Literature Survey**
   - 2.1 Evolution of AI Assistants and Tool Use
   - 2.2 Model Context Protocol (MCP) Standards
   - 2.3 Comparison: Custom Plugins vs. Open MCP Servers
   - 2.4 Security Risks in LLM Tool Execution
3. **Chapter 3: System Analysis and Requirements**
   - 3.1 Existing System and Its Limitations
   - 3.2 Proposed System
   - 3.3 Functional Requirements
   - 3.4 Non-Functional Requirements
   - 3.5 Software and Hardware Specifications
   - 3.6 Feasibility Study
4. **Chapter 4: System Design**
   - 4.1 System Architecture
   - 4.2 Data Flow Diagrams (DFD Level 0 and Level 1)
   - 4.3 Use Case Diagram and Specifications
   - 4.4 Flowcharts (Read Request Flow & Dry-Run Confirmation Flow)
   - 4.5 Tool Schema and Parameter Design
5. **Chapter 5: Implementation**
   - 5.1 Technology Stack Rationale
   - 5.2 Modular Code Organization
   - 5.3 Authentication and Secret Hygiene
   - 5.4 Handling Pagination and Rate Limits
   - 5.5 Stderr Logging for Protocol Integrity
   - 5.6 Dry-Run Confirmation Pattern for Write Operations
6. **Chapter 6: Testing and Results**
   - 6.1 Unit and Integration Testing
   - 6.2 The 50-Question Benchmark Dataset
   - 6.3 Evaluation Methodology (Round 1 vs. Round 2)
   - 6.4 Results and Quantitative Metrics
   - 6.5 Failure Analysis and Prompt Disambiguation
7. **Chapter 7: Conclusion and Future Scope**
   - 7.1 Conclusion
   - 7.2 Personal Learnings
   - 7.3 Future Enhancements
8. **References**

---

# CHAPTER 1: INTRODUCTION

### 1.1 Problem Statement
Modern Large Language Models (LLMs) such as Claude, GPT-4, and Gemini have demonstrated strong reasoning capabilities over public information. However, they are isolated from private, authenticated user environments. A software developer cannot ask an AI assistant basic questions about their private codebases, such as:
- *"How many open issues do I have across all my repositories?"*
- *"Which of my issues have been inactive for over a month?"*
- *"Summarize recent commits and open PRs for my project."*

Because this data resides behind GitHub authentication, standard web-search enabled models fail. Developers are forced to manually switch between their terminal, browser tabs, and AI chat interfaces, disrupting development workflow.

### 1.2 Motivation
Until recently, connecting an LLM to external APIs required building bespoke chatbots or vendor-locked plugins. The Model Context Protocol (MCP), open-sourced by Anthropic, introduces a standardized, universal interface for exposing tools and resources to AI models. Building an MCP server for GitHub provides an ideal opportunity to understand the infrastructure layer beneath modern AI systems: protocol transport, schema design, secure token scoping, rate-limiting, and evaluation of tool selection accuracy.

### 1.3 Project Objectives
1. **Design and build an open-standard MCP server in Python** that interfaces with the GitHub REST API.
2. **Follow a "Read-Only First" architectural philosophy**, implementing 5 comprehensive inspection tools.
3. **Implement state-changing write operations behind strict safety guardrails**, using a dry-run confirmation pattern where user approval is required prior to mutation.
4. **Enforce least-privilege security**, using fine-grained Personal Access Tokens (PATs) and strictly isolating credentials from source control.
5. **Benchmark and evaluate LLM tool selection reliability** using a 50-question dataset across English, Hindi, and Hinglish, demonstrating measurable before-and-after accuracy improvements through prompt refinement.

### 1.4 Scope and Boundaries
- **In Scope:**
  - Repository listing with visibility and sort filters (`list_repos`).
  - Repository issue inspection with label filters and PR exclusion (`list_open_issues`).
  - Cross-repository issue counting using GitHub Search API (`count_open_issues_all`).
  - Comprehensive repository activity dashboard (`get_repo_summary`).
  - Detection of neglected issues based on inactivity thresholds (`stale_issues`).
  - Safe issue creation with dry-run preview (`create_issue`).
  - Safe label assignment with dry-run preview (`add_label`).
  - Rate-limit detection and automatic pagination.
- **Out of Scope:**
  - Destructive delete actions (repositories, issues, branches) to prevent accidental data loss.
  - Multi-user authentication sessions (server is single-tenant local client).
  - Code search across raw file trees (excluded due to strict secondary rate limits of 10 requests/minute).

---

# CHAPTER 2: LITERATURE SURVEY

### 2.1 Evolution of AI Assistants and Tool Use
Early conversational agents were purely generative, relying solely on weights trained on static historical data. With the introduction of Tool Calling / Function Calling (Schick et al., 2023), language models were fine-tuned to emit structured JSON payloads representing function invocations when their internal knowledge proved insufficient.

### 2.2 Model Context Protocol (MCP) Standards
Historically, each AI platform maintained proprietary tool-calling specifications (e.g., OpenAI Assistants API, LangChain tools). In late 2024, the Model Context Protocol (MCP) was introduced as an open standard. MCP operates over standard input/output (`stdio`) or Server-Sent Events (`SSE`), defining strict JSON-RPC 2.0 request/response cycles for three primary primitives:
1. **Prompts:** Pre-defined templates for user interaction.
2. **Resources:** Read-only contextual data (files, schemas, documentation).
3. **Tools:** Executable routines that perform computations or interact with external APIs.

### 2.3 Comparison: Custom Plugins vs. Open MCP Servers
| Parameter | Proprietary Custom Plugins | MCP Server Architecture |
|---|---|---|
| **Ecosystem Portability** | Tied to a single AI vendor platform | Works across any MCP client (Claude Desktop, IDEs, CLI) |
| **Transport Layer** | Webhook / Remote REST endpoints | Standard `stdio` (local process) or `SSE` (network) |
| **Hosting Cost** | Requires cloud servers / public IP | Zero cost (runs locally on the user's machine) |
| **Credential Security** | Secrets often shared with third parties | Secrets remain strictly on the user's local machine |

### 2.4 Security Risks in LLM Tool Execution
Research on autonomous agent vulnerabilities highlights "Prompt Injection" and "Unintended Execution" as major risks. If an AI model is given unrestricted access to mutating tools, ambiguous input can trigger destructive actions. This project adopts defense-in-depth: read-only tools are unconstrained, while write tools default to preview mode and require explicit parameter flags (`confirm=True`) to execute.

---

# CHAPTER 3: SYSTEM ANALYSIS AND REQUIREMENTS

### 3.1 Existing System and Its Limitations
In the existing setup, developers manually browse github.com or run `gh` CLI commands to check issues, PRs, and commit logs. When using AI assistants to analyze project status, developers must copy-paste terminal logs into the chat window. This process is slow, repetitive, prone to human error, and lacks context awareness.

### 3.2 Proposed System
The proposed system implements a lightweight, local MCP server running alongside the client (Claude Desktop). When the user asks a natural language question, the AI model discovers available GitHub tools, selects the appropriate tool, populates parameters, and receives structured data over local `stdio` communication pipes without exposing credentials to external servers.

### 3.3 Functional Requirements
- **FR1: Repository Discovery:** The system shall retrieve all public and private repositories owned by the user.
- **FR2: Issue Inspection:** The system shall fetch open issues for a given repository, filtering out pull requests.
- **FR3: Cross-Repo Aggregation:** The system shall query total open issues across all user repositories in a single API call.
- **FR4: Repository Health Summary:** The system shall compile stars, forks, recent commits, and open PRs into a dashboard summary.
- **FR5: Stale Issue Detection:** The system shall identify issues with no updates for $N$ days.
- **FR6: Safe Issue Creation:** The system shall display a dry-run preview of an issue, creating it only when `confirm=True`.
- **FR7: Safe Labeling:** The system shall preview label additions, applying them only when `confirm=True`.

### 3.4 Non-Functional Requirements
- **NFR1: Zero Cost:** All components must use free, open-source software and GitHub's free API tiers.
- **NFR2: Least Privilege:** The system must function using a fine-grained PAT with access restricted to Issues, PRs, and Metadata.
- **NFR3: Protocol Reliability:** All server diagnostic messages must be sent to `sys.stderr` to prevent corrupting the `sys.stdout` JSON-RPC channel.
- **NFR4: Low Latency:** Common queries must respond within 1–2 seconds.

### 3.5 Software and Hardware Specifications
- **Operating System:** Windows 11 / 10, Linux, or macOS.
- **Runtime Environment:** Python 3.10+ (tested on Python 3.14.7).
- **Primary Dependencies:** `mcp` (v2.3.0), `httpx` (v0.28.1), `python-dotenv` (v1.2.4).
- **MCP Client:** Claude Desktop / MCP Inspector.
- **Hardware:** Standard PC/Laptop with minimum 4 GB RAM and internet connection.

### 3.6 Feasibility Study
- **Technical Feasibility:** The official Python MCP SDK and GitHub REST API v3 provide stable, documented APIs.
- **Economic Feasibility:** Software tools, Python libraries, GitHub API, and Claude Desktop free tier require zero financial budget.
- **Operational Feasibility:** Requires simple one-time configuration via `.env` file and `claude_desktop_config.json`.

---

# CHAPTER 4: SYSTEM DESIGN

### 4.1 System Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                         LOCAL HOST                            │
│                                                               │
│   ┌────────────────────┐     stdio (JSON-RPC)   ┌───────────┐ │
│   │     MCP Client     │ ◄════════════════════► │server.py  │ │
│   │  (Claude Desktop)  │                        └─────┬─────┘ │
│   └────────────────────┘                              │       │
│                                           Internal Python Call│
│                                                       ▼       │
│                                              ┌──────────────┐ │
│                                              │github_client │ │
│                                              └────────┬─────┘ │
└───────────────────────────────────────────────────────┼───────┘
                                                        │ HTTPS (Bearer Token)
                                                        ▼
                                             ┌─────────────────────┐
                                             │   GitHub REST API   │
                                             │  (api.github.com)   │
                                             └─────────────────────┘
```

### 4.2 Data Flow Diagrams (DFD)

#### Level 0 DFD (Context Diagram)
```
[User] ──(Natural Language Query)──► [GitHub MCP Server System] ──(Formatted Response)──► [User]
                                              │            ▲
                                 (HTTPS Req)  │            │ (JSON Data)
                                              ▼            │
                                     [GitHub REST API Service]
```

#### Level 1 DFD
```
[User Prompt]
     │
     ▼
(1.0 Tool Selection Engine - LLM) ──► Generates Tool Call Arguments
     │
     ▼
(2.0 MCP Protocol Dispatcher - server.py)
     │
     ├── If Write Tool & confirm == False ──► (2.1 Dry-Run Generator) ──► Return Preview
     │
     └── If Read Tool OR confirm == True
              │
              ▼
         (3.0 GitHub API Client - github_client.py)
              │
              ├── Checks X-RateLimit Headers
              ├── Appends Bearer Auth Header
              └── Handles HTTP Pagination Link Headers
              │
              ▼
         [api.github.com]
              │
              ▼
         (4.0 Output Formatter) ──► Clean Markdown Output to User
```

### 4.3 Use Case Diagram and Specifications

```
                       ┌─────────────────────────────────────────┐
                       │           GitHub MCP Server             │
                       │                                         │
                       │   (UC1: List Repositories)              │
                       │   (UC2: Inspect Open Issues)            │
     ┌──────────┐      │   (UC3: Count Issues Across Repos)      │      ┌────────────┐
     │          │ ───► │   (UC4: View Repository Summary)        │ ───► │   GitHub   │
     │   User   │      │   (UC5: Detect Stale Inactive Issues)   │      │  REST API  │
     │          │      │   (UC6: Preview / Create Issue)         │      └────────────┘
     └──────────┘      │   (UC7: Preview / Add Label)            │
                       │                                         │
                       └─────────────────────────────────────────┘
```

### 4.4 Flowcharts

#### A. Read Request Flowchart
```
[User asks Question] ──► [LLM selects Read Tool] ──► [Validate Inputs]
                                                             │
            ┌────────────────────────────────────────────────┘
            ▼
[Send GET Request to api.github.com]
            │
            ▼
[Check Response Status]
   ├── Status == 200 ──► [Filter PRs if Issues endpoint] ──► [Format text] ──► [Return Output]
   ├── Status == 401 ──► [Return Auth Error message]
   ├── Status == 404 ──► [Return Not Found message]
   └── Rate Limit 0  ──► [Return Reset Time wait message]
```

#### B. Dry-Run Confirmation Flowchart (Write Tools)
```
[User requests: "Create issue..."]
            │
            ▼
[LLM calls create_issue(confirm=False)]
            │
            ▼
[confirm == True ?]
   ├── NO  ──► [Generate Dry-Run Preview with Title, Repo, Labels] ──► [Display to User]
   │                                                                           │
   │                                                             (User confirms: "Yes")
   │                                                                           │
   └── YES ◄───────────────────────────────────────────────────────────────────┘
        │
        ▼
   [Send POST to api.github.com/repos/.../issues]
        │
        ▼
   [Return Success Message + Issue URL]
```

### 4.5 Tool Schema and Parameter Design
| Tool Name | Parameters | Return Type | Description |
|---|---|---|---|
| `list_repos` | `visibility: str`, `sort_by: str`, `limit: int` | `str` | Lists user's repositories with stats |
| `list_open_issues` | `owner: str`, `repo: str`, `label: str`, `limit: int` | `str` | Lists issues for a single repo (PRs excluded) |
| `count_open_issues_all`| `label: str` | `str` | Account-wide issue count using Search API |
| `get_repo_summary` | `owner: str`, `repo: str` | `str` | Dashboard view of commits, stars, PRs |
| `stale_issues` | `owner: str`, `repo: str`, `days: int` | `str` | Lists issues untouched for $N$ days |
| `create_issue` | `owner`, `repo`, `title`, `body`, `labels`, `confirm: bool` | `str` | Preview or create an issue |
| `add_label` | `owner`, `repo`, `issue_number`, `labels`, `confirm: bool` | `str` | Preview or attach labels to an issue |

---

# CHAPTER 5: IMPLEMENTATION

### 5.1 Technology Stack Rationale
- **Python 3.14**: High developer productivity, native asynchronous networking capabilities, and standard typing support.
- **Python MCP SDK (`mcp` v2.3.0)**: Anthropic's official SDK providing the `MCPServer` high-level abstraction and stdio transport loop.
- **`httpx` (v0.28.1)**: Modern HTTP client with strict timeout control and custom header support.
- **`python-dotenv` (v1.2.4)**: Zero-dependency environment variable parser keeping secrets isolated from the operating environment.

### 5.2 Modular Code Organization
The codebase separates concerns across three core modules:
1. `config.py`: Validates presence of `GITHUB_TOKEN` upon process startup; terminates with exit code 1 if missing.
2. `github_client.py`: Encapsulates HTTP transport, pagination parsing, authentication headers, rate-limit warnings, and raw response mapping.
3. `server.py`: Defines MCP tool declarations, docstring semantic interfaces, input bounds checking, dry-run safety branches, and clean text presentation.

### 5.3 Authentication and Secret Hygiene
Security follows the Principle of Least Privilege:
- Authentication uses a GitHub Fine-Grained Personal Access Token.
- Permissions are strictly confined to:
  - `Issues`: Read and Write
  - `Pull requests`: Read-only
  - `Metadata`: Read-only
- The token is placed inside `.env`. The project `.gitignore` explicitly excludes `.env`, `.venv/`, and `__pycache__/`.

### 5.4 Handling Pagination and Rate Limits
GitHub limits REST responses to a maximum of 100 items per request. `GitHubClient._get_paginated()` reads RFC 5988 `Link` headers:
```python
link_header = response.headers.get("link", "")
# Extracts URL where rel="next"
```
The client checks `X-RateLimit-Remaining` on every response. If remaining requests drop below 10, a warning is logged; if exhausted (0), the server calculates the reset window from `X-RateLimit-Reset` and raises a clean notification rather than crashing.

### 5.5 Stderr Logging for Protocol Integrity
In MCP stdio transport, `sys.stdout` is reserved strictly for JSON-RPC framing. Standard `print()` statements write to `stdout`, which immediately causes JSON parsing syntax errors in the client. To prevent protocol corruption, logging is configured explicitly:
```python
handler = logging.StreamHandler(sys.stderr)
logger.addHandler(handler)
```

### 5.6 Dry-Run Confirmation Pattern for Write Operations
To eliminate unintended data creation by AI agents, write tools enforce a 2-step verification protocol:
```python
if not confirm:
    return "DRY RUN — Issue preview (not created yet)... Call again with confirm=True."
# Actual GitHub API execution only reached when confirm=True
```

---

# CHAPTER 6: TESTING AND RESULTS

### 6.1 Unit and Integration Testing
Initial functional verification was conducted using automated scripts:
- `test_token.py`: Verified HTTP 200 authentication with GitHub API using fine-grained token.
- `test_all_tools.py`: Verified all 5 read tools and write dry-runs against live repository `pranjay6667/Pranjay`.
- `test_safety_quality.py`: Verified state changes under confirmed mode (`confirm=True`), successfully creating issue #7 and applying labels.

### 6.2 The 50-Question Benchmark Dataset
To evaluate how reliably an AI assistant selects the correct tool, a benchmark of 50 natural language prompts was curated in `evaluation/questions.csv`:
- **Direct Queries (20):** Explicit requests for specific actions (e.g., *"List all open issues in pranjay6667/Pranjay"*).
- **Multilingual Queries (15):** 9 Hinglish queries and 6 Hindi queries testing cross-lingual capability.
- **Ambiguous Queries (8):** Prompts where multiple tools could conceptually apply.
- **Out-of-Scope Queries (7):** Irrelevant prompts or unsupported destructive requests (e.g., *"Delete repository Pranjay"*).

### 6.3 Evaluation Methodology (Round 1 vs. Round 2)
The evaluation measured accuracy before and after optimizing tool descriptions:
- **Round 1 (Baseline / Naive Descriptions):** Generic docstrings (e.g., `count_open_issues_all` was described simply as *"Count issues"*).
- **Round 2 (Optimized Descriptions):** Docstrings enriched with boundary conditions, negative constraints, and explicit usage triggers.

### 6.4 Results and Quantitative Metrics
Testing was executed via `evaluation/evaluate.py`.

#### Overall Performance Summary
| Metric | Round 1 (Naive) | Round 2 (Optimized) | Improvement |
|---|---|---|---|
| **Total Test Queries** | 50 | 50 | — |
| **Correctly Routed Calls** | 45 | 49 | +4 calls |
| **Overall Accuracy** | **90.0%** | **98.0%** | **+8.0%** |
| **Error Rate** | 10.0% | 2.0% | -8.0% |

#### Category Breakdown
| Test Category | Count | Round 1 Accuracy | Round 2 Accuracy | Gain |
|---|---|---|---|---|
| **Direct Queries** | 20 | 100.0% | 100.0% | 0.0% |
| **Multilingual (Hindi/Hinglish)** | 15 | 100.0% | 100.0% | 0.0% |
| **Ambiguous / Boundary Cases** | 8 | 62.5% | **87.5%** | **+25.0%** |
| **Out-of-Scope / No Tool** | 7 | 71.4% | **100.0%** | **+28.6%** |

#### Language Performance Breakdown (Round 2)
- **English:** 32 / 33 correct (**97.0%**)
- **Hinglish:** 9 / 9 correct (**100.0%**)
- **Hindi:** 8 / 8 correct (**100.0%**)

### 6.5 Failure Analysis and Prompt Disambiguation
1. **Disambiguating Single-Repo vs. Account-Wide Counts:**
   - In Round 1, query *"How many issues are open in repo Pranjay?"* misrouted to `count_open_issues_all` due to the keyword "count".
   - In Round 2, the docstring was clarified: *"Use this tool when the user asks for a cross-repository overview across ALL repos. Do NOT use when a specific repo name is mentioned."* This resolved the misclassification.
2. **Preventing Destructive Action Hallucination:**
   - In Round 1, *"Delete repository Pranjay"* caused the model to hallucinate a call to `create_issue`.
   - In Round 2, server-level system instructions explicitly stated: *"This server does not provide deletion tools. Write tools are strictly limited to create_issue and add_label."* The model accurately refused to invoke any tool.

---

# CHAPTER 7: CONCLUSION AND FUTURE SCOPE

### 7.1 Conclusion
This project successfully designed, implemented, and benchmarked an open-standard GitHub Model Context Protocol (MCP) server in Python. The system provides AI assistants with secure, authenticated access to developer data across 7 purpose-built tools. By prioritizing a read-only architecture and enforcing dry-run confirmations on write tools, the server guarantees user safety. The experimental evaluation confirmed that prompt engineering on tool descriptions directly elevated tool selection accuracy from 90.0% to 98.0%.

### 7.2 Personal Learnings
- Gained hands-on proficiency in the Model Context Protocol (MCP) and JSON-RPC over `stdio` transport.
- Learned the critical importance of keeping `stdout` unpolluted and redirecting operational telemetry to `stderr`.
- Mastered defensive API programming: link-based pagination, rate-limit header monitoring, and fine-grained token authorization.
- Understood that tool descriptions serve as the machine API documentation for LLMs, directly dictating function calling accuracy.

### 7.3 Future Enhancements
- **OAuth 2.0 Web Flow:** Implement user authorization via web popup to eliminate manual token creation.
- **Local SQLite Caching:** Add lightweight caching with TTL to minimize redundant GitHub API calls.
- **Pull Request Management:** Expand write capabilities to include approving or reviewing open pull requests.

---

# REFERENCES

1. Anthropic. (2024). *Model Context Protocol Specification*. https://modelcontextprotocol.io/
2. GitHub Inc. (2024). *GitHub REST API Documentation*. https://docs.github.com/en/rest
3. Schick, T., et al. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools*. arXiv preprint arXiv:2302.04761.
4. Python Software Foundation. (2024). *The Python Standard Library — Logging and Subprocess Management*. https://docs.python.org/3/
5. Model Context Protocol Python SDK. (2024). *FastMCP and MCPServer Developer Guide*. https://py.sdk.modelcontextprotocol.io/
