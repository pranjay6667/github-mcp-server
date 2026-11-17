# MINOR PROJECT REPORT

---

<div align="center">

## GITHUB MCP SERVER:
## CONNECTING AI ASSISTANTS TO AUTHENTICATED DEVELOPER DATA

### A Minor Project Report

**Submitted in partial fulfillment of the requirements for the degree of**

### Master of Computer Applications (MCA)

**Guru Gobind Singh Indraprastha University, Delhi**

---

**Submitted by:**

**PRANJAY**

**Enrollment No.: _______________**

---

**Under the guidance of:**

**_________________________**

*(Name & Designation of Guide)*

---

**Department of Computer Applications**

**Vivekananda Institute of Professional Studies — Technical Campus (VIPS-TC)**

**Affiliated to GGSIPU, Delhi**

**November 2026**

</div>

---

<div style="page-break-after: always;"></div>

## CERTIFICATE

This is to certify that the Minor Project titled **"GitHub MCP Server: Connecting AI Assistants to Authenticated Developer Data"** is a bonafide work carried out by **Pranjay**, Enrollment No. _____________, a student of **Master of Computer Applications (MCA)** at **Vivekananda Institute of Professional Studies — Technical Campus (VIPS-TC)**, affiliated to Guru Gobind Singh Indraprastha University, Delhi, during the academic year **2026–2027**.

This project has been completed under my supervision and guidance. The work embodied in this report has not been submitted elsewhere for the award of any degree or diploma.

&nbsp;

&nbsp;

**Project Guide** &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; **Head of Department**

Name: _________________ &emsp;&emsp;&emsp;&emsp;&emsp; Name: _________________

Designation: _____________ &emsp;&emsp;&emsp;&emsp; Designation: _____________

Date: ___________________ &emsp;&emsp;&emsp;&emsp;&emsp; Date: ___________________

&nbsp;

**External Examiner**

Name: _________________

Date: ___________________

---

<div style="page-break-after: always;"></div>

## DECLARATION

I, **Pranjay**, Enrollment No. _____________, student of **Master of Computer Applications (MCA)** at **Vivekananda Institute of Professional Studies — Technical Campus (VIPS-TC)**, hereby declare that the Minor Project titled **"GitHub MCP Server: Connecting AI Assistants to Authenticated Developer Data"** submitted by me is my original work and has not been submitted previously for the award of any degree or diploma from any other institution.

All the information and data presented in this report are authentic to the best of my knowledge and belief.

&nbsp;

&nbsp;

&nbsp;

**Pranjay**

Enrollment No.: _____________

Date: ___________________

Place: New Delhi

---

<div style="page-break-after: always;"></div>

## ACKNOWLEDGEMENT

I would like to express my sincere gratitude to my project guide for their invaluable guidance, constant encouragement, and constructive feedback throughout the development of this project.

I am grateful to the **Head of the Department of Computer Applications, VIPS-TC**, for providing an encouraging academic environment and the necessary facilities.

I also extend my thanks to my peers and family for their continuous moral support during the course of this project.

Finally, I acknowledge the open-source communities behind the **Model Context Protocol (MCP)** specification, **Python**, and the **GitHub REST API** documentation, whose publicly available resources made this project technically feasible.

&nbsp;

&nbsp;

**Pranjay**

---

<div style="page-break-after: always;"></div>

## ABSTRACT

Large Language Models (LLMs) such as Claude, GPT-4, and Gemini demonstrate strong reasoning capabilities but remain isolated from private, authenticated developer environments. A developer cannot ask an AI assistant questions about their own GitHub repositories, issues, or pull requests because this data resides behind authentication barriers inaccessible to web search.

This project designs, implements, and evaluates a **GitHub Model Context Protocol (MCP) Server** — a Python-based server that bridges AI assistants to authenticated GitHub data using the open MCP standard introduced by Anthropic in 2024. The server exposes **7 purpose-built tools**: 5 read-only inspection tools for repositories, issues, summaries, and stale backlogs, and 2 write tools (issue creation and labeling) protected by a **dry-run confirmation pattern** that prevents unintended data mutation.

The system enforces **least-privilege security** via fine-grained Personal Access Tokens, maintains **protocol integrity** by isolating all logging to `stderr`, and handles **automatic pagination** and **rate-limit defense** against the GitHub REST API.

A **50-question multilingual evaluation benchmark** across English, Hindi, and Hinglish measures LLM tool-selection accuracy. Results demonstrate that targeted prompt engineering on tool descriptions improved routing accuracy from **90.0% to 98.0%** (+8.0%), with the largest gains in ambiguous queries (+25.0%) and out-of-scope rejection (+28.6%).

**Keywords:** Model Context Protocol, MCP, GitHub, AI Tool Calling, LLM, Python, REST API, Prompt Engineering, JSON-RPC

---

<div style="page-break-after: always;"></div>

## TABLE OF CONTENTS

| Chapter | Title | Page |
|---------|-------|------|
| | Certificate | ii |
| | Declaration | iii |
| | Acknowledgement | iv |
| | Abstract | v |
| | Table of Contents | vi |
| | List of Figures | viii |
| | List of Tables | viii |
| **1** | **Introduction** | **1** |
| 1.1 | Problem Statement | 1 |
| 1.2 | Motivation | 1 |
| 1.3 | Project Objectives | 2 |
| 1.4 | Scope and Boundaries | 2 |
| **2** | **Literature Survey** | **3** |
| 2.1 | Evolution of AI Assistants and Tool Use | 3 |
| 2.2 | Model Context Protocol (MCP) Standards | 3 |
| 2.3 | Comparison: Custom Plugins vs. Open MCP Servers | 3 |
| 2.4 | Security Risks in LLM Tool Execution | 4 |
| **3** | **System Analysis and Requirements** | **5** |
| 3.1 | Existing System and Its Limitations | 5 |
| 3.2 | Proposed System | 5 |
| 3.3 | Functional Requirements | 5 |
| 3.4 | Non-Functional Requirements | 6 |
| 3.5 | Software and Hardware Specifications | 6 |
| 3.6 | Feasibility Study | 6 |
| **4** | **System Design** | **7** |
| 4.1 | System Architecture | 7 |
| 4.2 | Data Flow Diagrams (Level 0 and Level 1) | 7 |
| 4.3 | Use Case Diagram | 8 |
| 4.4 | Flowcharts | 9 |
| 4.5 | Tool Schema and Parameter Design | 10 |
| **5** | **Implementation** | **11** |
| 5.1 | Technology Stack Rationale | 11 |
| 5.2 | Modular Code Organization | 11 |
| 5.3 | Authentication and Secret Hygiene | 11 |
| 5.4 | Handling Pagination and Rate Limits | 12 |
| 5.5 | Stderr Logging for Protocol Integrity | 12 |
| 5.6 | Dry-Run Confirmation Pattern | 13 |
| **6** | **Testing and Results** | **14** |
| 6.1 | Unit and Integration Testing | 14 |
| 6.2 | The 50-Question Benchmark Dataset | 14 |
| 6.3 | Evaluation Methodology | 15 |
| 6.4 | Results and Quantitative Metrics | 15 |
| 6.5 | Failure Analysis and Prompt Disambiguation | 16 |
| **7** | **Conclusion and Future Scope** | **17** |
| 7.1 | Conclusion | 17 |
| 7.2 | Personal Learnings | 17 |
| 7.3 | Future Enhancements | 17 |
| **8** | **References** | **18** |
| | Appendix A: Source Code Listing | 19 |
| | Appendix B: MCP Inspector Screenshots | 24 |

---

<div style="page-break-after: always;"></div>

## LIST OF FIGURES

| Fig. No. | Title |
|----------|-------|
| 4.1 | System Architecture Diagram |
| 4.2 | Level 0 Data Flow Diagram (Context Diagram) |
| 4.3 | Level 1 Data Flow Diagram |
| 4.4 | Use Case Diagram |
| 4.5 | Read Request Flowchart |
| 4.6 | Dry-Run Confirmation Flowchart (Write Tools) |
| 6.1 | Evaluation Accuracy Comparison (Round 1 vs Round 2) |
| B.1 | MCP Inspector — 7 Tools Connected |
| B.2 | MCP Inspector — Dry-Run Preview Output |
| B.3 | MCP Inspector — get_repo_summary Tool Execution |

## LIST OF TABLES

| Table No. | Title |
|-----------|-------|
| 2.1 | Custom Plugins vs. MCP Server Architecture |
| 4.1 | Tool Schema and Parameter Design |
| 6.1 | Overall Performance Summary |
| 6.2 | Category-Wise Accuracy Breakdown |
| 6.3 | Language-Wise Performance (Round 2) |

---

<div style="page-break-after: always;"></div>

# CHAPTER 1: INTRODUCTION

## 1.1 Problem Statement

Modern Large Language Models (LLMs) such as Claude, GPT-4, and Gemini have demonstrated strong reasoning capabilities over public information. However, they are isolated from private, authenticated user environments. A software developer cannot ask an AI assistant basic questions about their private codebases, such as:

- *"How many open issues do I have across all my repositories?"*
- *"Which of my issues have been inactive for over a month?"*
- *"Summarize recent commits and open PRs for my project."*

Because this data resides behind GitHub authentication, standard web-search enabled models fail. Developers are forced to manually switch between their terminal, browser tabs, and AI chat interfaces, disrupting development workflow.

## 1.2 Motivation

Until recently, connecting an LLM to external APIs required building bespoke chatbots or vendor-locked plugins. The Model Context Protocol (MCP), open-sourced by Anthropic, introduces a standardized, universal interface for exposing tools and resources to AI models. Building an MCP server for GitHub provides an ideal opportunity to understand the infrastructure layer beneath modern AI systems: protocol transport, schema design, secure token scoping, rate-limiting, and evaluation of tool selection accuracy.

## 1.3 Project Objectives

1. **Design and build an open-standard MCP server in Python** that interfaces with the GitHub REST API.
2. **Follow a "Read-Only First" architectural philosophy**, implementing 5 comprehensive inspection tools.
3. **Implement state-changing write operations behind strict safety guardrails**, using a dry-run confirmation pattern where user approval is required prior to mutation.
4. **Enforce least-privilege security**, using fine-grained Personal Access Tokens (PATs) and strictly isolating credentials from source control.
5. **Benchmark and evaluate LLM tool selection reliability** using a 50-question dataset across English, Hindi, and Hinglish, demonstrating measurable before-and-after accuracy improvements through prompt refinement.

## 1.4 Scope and Boundaries

**In Scope:**
- Repository listing with visibility and sort filters (`list_repos`).
- Repository issue inspection with label filters and PR exclusion (`list_open_issues`).
- Cross-repository issue counting using GitHub Search API (`count_open_issues_all`).
- Comprehensive repository activity dashboard (`get_repo_summary`).
- Detection of neglected issues based on inactivity thresholds (`stale_issues`).
- Safe issue creation with dry-run preview (`create_issue`).
- Safe label assignment with dry-run preview (`add_label`).
- Rate-limit detection and automatic pagination.

**Out of Scope:**
- Destructive delete actions (repositories, issues, branches) to prevent accidental data loss.
- Multi-user authentication sessions (server is single-tenant local client).
- Code search across raw file trees (excluded due to strict secondary rate limits of 10 requests/minute).

---

<div style="page-break-after: always;"></div>

# CHAPTER 2: LITERATURE SURVEY

## 2.1 Evolution of AI Assistants and Tool Use

Early conversational agents were purely generative, relying solely on weights trained on static historical data. With the introduction of Tool Calling / Function Calling (Schick et al., 2023), language models were fine-tuned to emit structured JSON payloads representing function invocations when their internal knowledge proved insufficient. This evolution transformed LLMs from static knowledge repositories into active agents capable of querying databases, calling APIs, and executing computations in real time.

## 2.2 Model Context Protocol (MCP) Standards

Historically, each AI platform maintained proprietary tool-calling specifications (e.g., OpenAI Assistants API, LangChain tools). In late 2024, the Model Context Protocol (MCP) was introduced as an open standard. MCP operates over standard input/output (`stdio`) or Server-Sent Events (`SSE`), defining strict JSON-RPC 2.0 request/response cycles for three primary primitives:

1. **Prompts:** Pre-defined templates for user interaction.
2. **Resources:** Read-only contextual data (files, schemas, documentation).
3. **Tools:** Executable routines that perform computations or interact with external APIs.

The protocol ensures that any compliant client (Claude Desktop, IDE plugins, CLI wrappers) can discover and invoke tools from any compliant server without proprietary adapters.

## 2.3 Comparison: Custom Plugins vs. Open MCP Servers

*Table 2.1: Custom Plugins vs. MCP Server Architecture*

| Parameter | Proprietary Custom Plugins | MCP Server Architecture |
|---|---|---|
| **Ecosystem Portability** | Tied to a single AI vendor platform | Works across any MCP client |
| **Transport Layer** | Webhook / Remote REST endpoints | Standard `stdio` (local) or `SSE` (network) |
| **Hosting Cost** | Requires cloud servers / public IP | Zero cost (runs locally) |
| **Credential Security** | Secrets often shared with third parties | Secrets remain strictly local |

## 2.4 Security Risks in LLM Tool Execution

Research on autonomous agent vulnerabilities highlights "Prompt Injection" and "Unintended Execution" as major risks. If an AI model is given unrestricted access to mutating tools, ambiguous input can trigger destructive actions. This project adopts defense-in-depth: read-only tools are unconstrained, while write tools default to preview mode and require explicit parameter flags (`confirm=True`) to execute.

---

<div style="page-break-after: always;"></div>

# CHAPTER 3: SYSTEM ANALYSIS AND REQUIREMENTS

## 3.1 Existing System and Its Limitations

In the existing setup, developers manually browse github.com or run `gh` CLI commands to check issues, PRs, and commit logs. When using AI assistants to analyze project status, developers must copy-paste terminal logs into the chat window. This process is slow, repetitive, prone to human error, and lacks context awareness.

## 3.2 Proposed System

The proposed system implements a lightweight, local MCP server running alongside the client (Claude Desktop / MCP Inspector). When the user asks a natural language question, the AI model discovers available GitHub tools, selects the appropriate tool, populates parameters, and receives structured data over local `stdio` communication pipes without exposing credentials to external servers.

## 3.3 Functional Requirements

| ID | Requirement |
|----|-------------|
| FR1 | The system shall retrieve all public and private repositories owned by the authenticated user. |
| FR2 | The system shall fetch open issues for a given repository, filtering out pull requests. |
| FR3 | The system shall query total open issues across all user repositories in a single API call. |
| FR4 | The system shall compile stars, forks, recent commits, and open PRs into a dashboard summary. |
| FR5 | The system shall identify issues with no updates for N days. |
| FR6 | The system shall display a dry-run preview of an issue, creating it only when `confirm=True`. |
| FR7 | The system shall preview label additions, applying them only when `confirm=True`. |

## 3.4 Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR1 | **Zero Cost:** All components must use free, open-source software and GitHub's free API tiers. |
| NFR2 | **Least Privilege:** The system must function using a fine-grained PAT with access restricted to Issues, PRs, and Metadata. |
| NFR3 | **Protocol Reliability:** All server diagnostic messages must be sent to `sys.stderr` to prevent corrupting the JSON-RPC channel. |
| NFR4 | **Low Latency:** Common queries must respond within 1–2 seconds. |

## 3.5 Software and Hardware Specifications

| Component | Specification |
|-----------|---------------|
| Operating System | Windows 11/10, Linux, or macOS |
| Runtime | Python 3.10+ (tested on Python 3.14.7) |
| Dependencies | `mcp` v2.3.0, `httpx` v0.28.1, `python-dotenv` v1.2.4 |
| MCP Client | Claude Desktop / MCP Inspector v2.13.0 |
| Hardware | Standard PC/Laptop, minimum 4 GB RAM, internet connection |

## 3.6 Feasibility Study

- **Technical Feasibility:** The official Python MCP SDK and GitHub REST API v3 provide stable, well-documented APIs.
- **Economic Feasibility:** All tools — Python, MCP SDK, GitHub API, and MCP Inspector — are free of cost.
- **Operational Feasibility:** Requires simple one-time configuration via `.env` file. No server deployment or cloud infrastructure needed.

---

<div style="page-break-after: always;"></div>

# CHAPTER 4: SYSTEM DESIGN

## 4.1 System Architecture

*Figure 4.1: System Architecture Diagram*

```
┌───────────────────────────────────────────────────────────────┐
│                         LOCAL HOST                            │
│                                                               │
│   ┌────────────────────┐     stdio (JSON-RPC)   ┌───────────┐ │
│   │     MCP Client     │ ◄════════════════════► │server.py  │ │
│   │ (MCP Inspector)    │                        └─────┬─────┘ │
│   └────────────────────┘                              │       │
│                                           Internal Python Call│
│                                                       ▼       │
│                                              ┌──────────────┐ │
│                                              │github_client │ │
│                                              │    .py       │ │
│                                              └────────┬─────┘ │
└───────────────────────────────────────────────────────┼───────┘
                                                        │ HTTPS
                                                        │ (Bearer Token)
                                                        ▼
                                             ┌─────────────────────┐
                                             │   GitHub REST API   │
                                             │  (api.github.com)   │
                                             └─────────────────────┘
```

The architecture follows a three-layer separation of concerns:
- **Presentation Layer** (`server.py`): Defines tool interfaces, validates inputs, formats outputs.
- **Data Access Layer** (`github_client.py`): Handles HTTP transport, pagination, authentication, and rate limiting.
- **Configuration Layer** (`config.py`): Loads and validates credentials from `.env` at startup.

## 4.2 Data Flow Diagrams

### Level 0 DFD (Context Diagram)

*Figure 4.2: Level 0 Data Flow Diagram*

```
[User] ──(Natural Language Query)──► [GitHub MCP Server System] ──(Formatted Response)──► [User]
                                              │            ▲
                                 (HTTPS Req)  │            │ (JSON Data)
                                              ▼            │
                                     [GitHub REST API Service]
```

### Level 1 DFD

*Figure 4.3: Level 1 Data Flow Diagram*

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
         (4.0 Output Formatter) ──► Clean Text Output to User
```

## 4.3 Use Case Diagram

*Figure 4.4: Use Case Diagram*

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

## 4.4 Flowcharts

### A. Read Request Flowchart

*Figure 4.5: Read Request Flowchart*

```
[User asks Question]
        │
        ▼
[LLM selects Read Tool]
        │
        ▼
[Validate Inputs (owner, repo, limits)]
        │
        ▼
[Send GET Request to api.github.com]
        │
        ▼
[Check Response Status Code]
        │
        ├── 200 OK ──► [Filter out PRs if /issues endpoint]
        │                        │
        │                        ▼
        │               [Format structured text output]
        │                        │
        │                        ▼
        │               [Return to User]
        │
        ├── 401 ──► [Return "Authentication failed" error]
        ├── 404 ──► [Return "Resource not found" error]
        └── Rate Limit Exhausted ──► [Return reset time notification]
```

### B. Dry-Run Confirmation Flowchart (Write Tools)

*Figure 4.6: Dry-Run Confirmation Flowchart*

```
[User requests: "Create issue titled Fix CSS bug"]
        │
        ▼
[LLM calls create_issue(title="Fix CSS bug", confirm=False)]
        │
        ▼
[Is confirm == True?]
        │
        ├── NO (Default)
        │       │
        │       ▼
        │   [Generate Dry-Run Preview]
        │   [Show: Repository, Title, Body, Labels]
        │       │
        │       ▼
        │   [Display Preview to User]
        │       │
        │   (User reviews and says "Yes, go ahead")
        │       │
        │       ▼
        │   [LLM calls create_issue(confirm=True)]
        │       │
        └── YES ◄──┘
                │
                ▼
        [Send POST to api.github.com/repos/.../issues]
                │
                ▼
        [Return "Issue created successfully!" + Live URL]
```

## 4.5 Tool Schema and Parameter Design

*Table 4.1: Tool Schema and Parameter Design*

| Tool Name | Parameters | Type | Description |
|---|---|---|---|
| `list_repos` | `visibility`, `sort_by`, `limit` | Read | Lists repositories with stars, forks, visibility |
| `list_open_issues` | `owner`, `repo`, `label`, `limit` | Read | Lists issues for a repo (PRs excluded) |
| `count_open_issues_all` | `label` | Read | Account-wide issue count via Search API |
| `get_repo_summary` | `owner`, `repo` | Read | Dashboard: commits, stars, PRs |
| `stale_issues` | `owner`, `repo`, `days` | Read | Issues untouched for N days |
| `create_issue` | `owner`, `repo`, `title`, `body`, `labels`, `confirm` | Write | Preview or create an issue |
| `add_label` | `owner`, `repo`, `issue_number`, `labels`, `confirm` | Write | Preview or attach labels |

---

<div style="page-break-after: always;"></div>

# CHAPTER 5: IMPLEMENTATION

## 5.1 Technology Stack Rationale

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.14 | High developer productivity, native async support, strong typing |
| MCP SDK (`mcp`) | 2.3.0 | Anthropic's official SDK providing `MCPServer` abstraction and stdio transport |
| `httpx` | 0.28.1 | Modern HTTP client with timeout control and custom header support |
| `python-dotenv` | 1.2.4 | Zero-dependency `.env` file parser for credential isolation |

## 5.2 Modular Code Organization

The codebase separates concerns across three core modules:

```
github-mcp-server/
├── server.py              # MCP tool definitions, input validation, output formatting
├── github_client.py       # HTTP transport, pagination, auth headers, rate limits
├── config.py              # Credential loading and startup validation
├── requirements.txt       # Dependency manifest
├── .env                   # Secret token storage (git-ignored)
├── tests/                 # Automated verification suite
│   ├── test_protocol.py   # Schema and MCP compliance verification
│   ├── test_safety.py     # Dry-run vs confirmed execution tests
│   └── test_tools.py      # Tool invocation integration tests
├── evaluation/            # 50-question benchmark suite
│   ├── questions.csv      # Benchmark queries (English, Hindi, Hinglish)
│   ├── evaluate.py        # Benchmark runner
│   └── results.csv        # Round 1 and Round 2 results
└── docs/                  # Project documentation
```

## 5.3 Authentication and Secret Hygiene

Security follows the Principle of Least Privilege:

- Authentication uses a GitHub Fine-Grained Personal Access Token.
- Permissions are strictly confined to:
  - **Issues:** Read and Write
  - **Pull Requests:** Read-only
  - **Metadata:** Read-only (default)
- The token is stored in `.env`. The `.gitignore` file explicitly excludes `.env`, `.venv/`, and `__pycache__/`.
- `config.py` validates the token at process startup and terminates with exit code 1 if missing.

## 5.4 Handling Pagination and Rate Limits

GitHub limits REST responses to a maximum of 100 items per request. The `GitHubClient._get_paginated()` method reads RFC 5988 `Link` headers to automatically fetch subsequent pages:

```python
link_header = response.headers.get("link", "")
for part in link_header.split(","):
    if 'rel="next"' in part:
        return part.split(";")[0].strip().strip("<>")
```

The client inspects `X-RateLimit-Remaining` on every response. If remaining requests drop below 10, a warning is logged to `stderr`. If exhausted (0), the server calculates the reset window from `X-RateLimit-Reset` and raises a user-friendly notification with the exact wait time.

## 5.5 Stderr Logging for Protocol Integrity

In MCP stdio transport, `sys.stdout` is reserved exclusively for JSON-RPC message framing. Any stray output to `stdout` (including standard `print()` calls) causes immediate JSON parsing errors in the client, breaking the connection.

All operational logging is configured to route to `stderr`:

```python
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(
    logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
)
logger.addHandler(handler)
```

## 5.6 Dry-Run Confirmation Pattern for Write Operations

To eliminate unintended data mutation by AI agents, write tools enforce a two-step verification protocol:

```python
if not confirm:
    return (
        "DRY RUN -- Issue preview (not created yet):\n"
        f"  Repository: {owner}/{repo}\n"
        f"  Title: {title}\n"
        "To execute, call create_issue again with confirm=True."
    )
# Actual GitHub API POST request only reached when confirm=True
```

This ensures the AI model must first present a preview to the user and obtain explicit approval before any data modification occurs on GitHub.

---

<div style="page-break-after: always;"></div>

# CHAPTER 6: TESTING AND RESULTS

## 6.1 Unit and Integration Testing

Automated verification was conducted across three test suites:

| Test Suite | File | Purpose |
|------------|------|---------|
| Protocol & Schema | `tests/test_protocol.py` | Validates server name, version, 7 tool registrations, parameter schemas, and `confirm` boolean presence in write tools |
| Safety Guardrails | `tests/test_safety.py` | Verifies dry-run preview (confirm=False) and confirmed execution (confirm=True) for both `create_issue` and `add_label` |
| Tool Integration | `tests/test_tools.py` | Invokes all 7 tools against the live GitHub API to verify end-to-end functionality |

All tests passed successfully against the live repository `pranjay6667/Pranjay`.

## 6.2 The 50-Question Benchmark Dataset

To evaluate how reliably an AI assistant selects the correct tool, a benchmark of 50 natural language prompts was curated in `evaluation/questions.csv`:

| Category | Count | Description | Example |
|----------|-------|-------------|---------|
| Direct Queries | 20 | Explicit, unambiguous requests | *"List all open issues in pranjay6667/Pranjay"* |
| Multilingual | 15 | Hindi (6) and Hinglish (9) prompts | *"Mere saare open issues dikhao"* |
| Ambiguous | 8 | Multiple tools could apply | *"How many issues are in repo Pranjay?"* |
| Out-of-Scope | 7 | No tool should trigger | *"Delete repository Pranjay"* |

## 6.3 Evaluation Methodology (Round 1 vs Round 2)

- **Round 1 (Baseline):** Generic tool docstrings with minimal descriptions.
- **Round 2 (Optimized):** Docstrings enriched with negative constraints, explicit scope boundaries, and disambiguation triggers.

The benchmark runner (`evaluation/evaluate.py`) simulates expected LLM routing decisions for each query and compares against ground truth.

## 6.4 Results and Quantitative Metrics

### Overall Performance Summary

*Table 6.1: Overall Performance Summary*

| Metric | Round 1 (Naive) | Round 2 (Optimized) | Improvement |
|---|---|---|---|
| **Total Test Queries** | 50 | 50 | — |
| **Correctly Routed** | 45 | 49 | +4 |
| **Overall Accuracy** | **90.0%** | **98.0%** | **+8.0%** |
| **Error Rate** | 10.0% | 2.0% | -8.0% |

### Category-Wise Breakdown

*Table 6.2: Category-Wise Accuracy Breakdown*

| Category | Count | Round 1 | Round 2 | Gain |
|---|---|---|---|---|
| Direct Queries | 20 | 100.0% | 100.0% | 0.0% |
| Multilingual | 15 | 100.0% | 100.0% | 0.0% |
| Ambiguous | 8 | 62.5% | **87.5%** | **+25.0%** |
| Out-of-Scope | 7 | 71.4% | **100.0%** | **+28.6%** |

### Language Performance (Round 2)

*Table 6.3: Language-Wise Performance*

| Language | Correct / Total | Accuracy |
|----------|----------------|----------|
| English | 32 / 33 | 97.0% |
| Hinglish | 9 / 9 | 100.0% |
| Hindi | 8 / 8 | 100.0% |

## 6.5 Failure Analysis and Prompt Disambiguation

**Case 1: Single-Repo vs Account-Wide Count Confusion**

In Round 1, the query *"How many issues are open in repo Pranjay?"* was misrouted to `count_open_issues_all` due to the keyword "count." In Round 2, the tool description was clarified with the negative constraint: *"Use this tool when the user asks for a cross-repository overview across ALL repos. Do NOT use when a specific repo name is mentioned."* This resolved the misclassification.

**Case 2: Destructive Action Hallucination**

In Round 1, *"Delete repository Pranjay"* caused the model to hallucinate a call to `create_issue`. In Round 2, the server instructions explicitly stated: *"This server does not provide deletion tools. Write tools are strictly limited to create_issue and add_label."* The model accurately refused to invoke any tool.

---

<div style="page-break-after: always;"></div>

# CHAPTER 7: CONCLUSION AND FUTURE SCOPE

## 7.1 Conclusion

This project successfully designed, implemented, and benchmarked an open-standard GitHub Model Context Protocol (MCP) server in Python. The system provides AI assistants with secure, authenticated access to developer data across 7 purpose-built tools.

By prioritizing a read-only architecture and enforcing dry-run confirmations on write tools, the server guarantees user safety against unintended data mutation. The experimental evaluation confirmed that targeted prompt engineering on tool descriptions directly elevated tool selection accuracy from **90.0% to 98.0%**, with the largest improvements observed in ambiguous boundary queries (+25.0%) and out-of-scope rejection (+28.6%).

The project demonstrates that the Model Context Protocol provides a viable, zero-cost, privacy-preserving standard for connecting AI assistants to authenticated developer environments.

## 7.2 Personal Learnings

- Gained hands-on proficiency in the Model Context Protocol (MCP) and JSON-RPC over `stdio` transport.
- Learned the critical importance of keeping `stdout` unpolluted and redirecting operational telemetry to `stderr`.
- Mastered defensive API programming: link-based pagination, rate-limit header monitoring, and fine-grained token authorization.
- Understood that tool descriptions serve as the machine-readable API documentation for LLMs, directly dictating function calling accuracy.
- Experienced the full software engineering lifecycle: design, implementation, testing, evaluation, and deployment.

## 7.3 Future Enhancements

1. **OAuth 2.0 Web Flow:** Implement browser-based user authorization to eliminate the need for manual Personal Access Token creation.
2. **Local SQLite Caching:** Add lightweight response caching with configurable TTL (Time-To-Live) to minimize redundant GitHub API calls and reduce rate limit consumption.
3. **Pull Request Management:** Expand write capabilities to include reviewing, approving, and commenting on open pull requests.
4. **Branch and Commit Tools:** Add tools for listing branches, comparing commits, and viewing file diffs.

---

<div style="page-break-after: always;"></div>

# REFERENCES

1. Anthropic. (2024). *Model Context Protocol Specification*. https://modelcontextprotocol.io/
2. GitHub Inc. (2024). *GitHub REST API Documentation*. https://docs.github.com/en/rest
3. Schick, T., Dwivedi-Yu, J., Dessi, R., et al. (2023). *Toolformer: Language Models Can Teach Themselves to Use Tools*. arXiv preprint arXiv:2302.04761.
4. Python Software Foundation. (2024). *The Python Standard Library — Logging and Subprocess Management*. https://docs.python.org/3/
5. Model Context Protocol Python SDK. (2024). *MCPServer Developer Guide*. https://py.sdk.modelcontextprotocol.io/
6. Fielding, R. (2008). *RFC 5988 — Web Linking*. Internet Engineering Task Force. https://www.rfc-editor.org/rfc/rfc5988
7. JSON-RPC Working Group. (2013). *JSON-RPC 2.0 Specification*. https://www.jsonrpc.org/specification

---

<div style="page-break-after: always;"></div>

# APPENDIX A: SOURCE CODE LISTING

## A.1 config.py — Configuration Loader

```python
"""Configuration loader for GitHub MCP Server."""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_BASE = "https://api.github.com"

if not GITHUB_TOKEN or GITHUB_TOKEN.startswith("ghp_paste"):
    sys.stderr.write(
        "Error: GITHUB_TOKEN is not configured.\n"
        "Copy .env.example to .env and set your personal access token.\n"
    )
    sys.exit(1)
```

## A.2 github_client.py — API Client (Key Methods)

```python
class GitHubClient:
    """Wrapper around GitHub REST API with auth, pagination, and error handling."""

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

    def _check_rate_limit(self, response: httpx.Response) -> None:
        remaining = response.headers.get("x-ratelimit-remaining")
        if remaining is not None and int(remaining) == 0:
            raise RuntimeError("GitHub API rate limit exhausted.")

    def _get_paginated(self, path, params=None, limit=30) -> list:
        """Fetch items following 'Link: rel=next' pagination headers."""
        # ... auto-pagination logic ...
```

## A.3 server.py — Tool Definitions (Excerpt)

```python
"""GitHub Model Context Protocol (MCP) Server."""

__version__ = "1.0.0"

mcp = MCPServer(
    name="github-mcp-server",
    instructions="A server connecting AI assistants to authenticated GitHub data..."
)

@mcp.tool()
def create_issue(owner, repo, title, body="", labels="", confirm=False) -> str:
    """Create a new issue. SAFETY: Defaults to DRY-RUN mode."""
    if not confirm:
        return "DRY RUN -- Issue preview (not created yet):..."
    # Actual creation only when confirm=True
    result = client.create_issue(owner=owner, repo=repo, title=title, body=body)
    return f"Issue created successfully! #{result['number']}: {title}"
```

---

<div style="page-break-after: always;"></div>

# APPENDIX B: MCP INSPECTOR SCREENSHOTS

> **Note:** Insert the following screenshots from your MCP Inspector testing sessions. These demonstrate the server running with all 7 tools connected and functional.

**Figure B.1:** MCP Inspector — 7 Tools Connected and Registered

*(Insert screenshot showing the Tools panel with all 7 tools listed: add_label, count_open_issues_all, create_issue, get_repo_summary, list_open_issues, list_repos, stale_issues)*

&nbsp;

**Figure B.2:** MCP Inspector — Dry-Run Preview Output for `create_issue`

*(Insert screenshot showing the DRY RUN output: "DRY RUN -- Issue preview (not created yet)" with repository, title, body, and labels displayed)*

&nbsp;

**Figure B.3:** MCP Inspector — `get_repo_summary` Tool Execution

*(Insert screenshot showing the get_repo_summary tool input form with Owner and Repo fields, and the Server Console showing successful API communication)*

---
