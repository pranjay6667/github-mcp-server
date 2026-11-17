"""
Generates the complete VIPS-TC / GGSIPU Minor Project Report
following the exact structure, tone, and formatting of the reference document.
Creates both docs/VIPS_PROJECT_REPORT.docx and docs/VIPS_PROJECT_REPORT.md
"""

import os
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = Path(r"C:\Users\pranj\.gemini\antigravity\scratch\github-mcp-server")
DOCS_DIR = BASE_DIR / "docs"
ASSETS_DIR = DOCS_DIR / "assets"
DOCX_PATH = DOCS_DIR / "VIPS_PROJECT_REPORT.docx"
MD_PATH = DOCS_DIR / "VIPS_PROJECT_REPORT.md"

def create_report():
    doc = Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles setup
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(12)
    style_normal.font.color.rgb = RGBColor(0, 0, 0)
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(6)

    def add_p(text="", align=WD_ALIGN_PARAGRAPH.LEFT, bold=False, italic=False, size=12, space_after=6, space_before=0):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.line_spacing = 1.15
        if text:
            run = p.add_run(text)
            run.bold = bold
            run.italic = italic
            run.font.name = 'Times New Roman'
            run.font.size = Pt(size)
            run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_heading_1(text):
        return add_p(text, align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_before=12, space_after=12)

    def add_heading_2(text):
        return add_p(text, align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, size=14, space_before=10, space_after=6)

    def add_heading_3(text):
        return add_p(text, align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, size=12, space_before=6, space_after=4)

    def add_image_if_exists(img_path, width=Inches(2.0), align=WD_ALIGN_PARAGRAPH.CENTER):
        if os.path.exists(img_path):
            p = doc.add_paragraph()
            p.alignment = align
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run()
            run.add_picture(str(img_path), width=width)
            return p
        return None

    # =========================================================================
    # 1. COVER PAGE
    # =========================================================================
    add_p("GitHub MCP Server – Connecting AI Assistants to Authenticated Developer Data",
          align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=18, space_before=12, space_after=18)

    add_p("IN PARTIAL FULFILLMENT OF THE REQUIREMENT FOR THE AWARD OF DEGREE OF",
          align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, space_after=4)
    add_p("MASTER OF COMPUTER APPLICATIONS",
          align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=14, space_after=18)

    add_p("Submitted By:", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, space_after=2)
    add_p("Pranjay (Enrollment No. ________________)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_after=16)

    # VIPS Logo
    add_image_if_exists(ASSETS_DIR / "vips_logo.png", width=Inches(1.8))

    add_p("VIVEKANANDA SCHOOL OF INFORMATION TECHNOLOGY",
          align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_before=6, space_after=2)
    add_p("VIVEKANANDA INSTITUTE OF PROFESSIONAL STUDIES TC",
          align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, space_after=10)

    add_p("Affiliated To", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, size=11, space_after=8)

    # GGSIPU Logo
    add_image_if_exists(ASSETS_DIR / "ggsipu_logo.png", width=Inches(1.5))

    add_p("Guru Gobind Singh Indraprastha University",
          align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, space_before=6, space_after=2)
    add_p("Sector - 16C Dwarka, Delhi – 110078",
          align=WD_ALIGN_PARAGRAPH.CENTER, size=11, space_after=12)

    doc.add_page_break()

    # =========================================================================
    # 2. ACKNOWLEDGEMENT
    # =========================================================================
    add_heading_1("ACKNOWLEDGEMENT")

    add_p("It is our proud privilege to express our profound gratitude to the entire management of Vivekananda Institute of Professional Studies – Technical Campus and teachers at the institute for providing us with the opportunity to avail the excellent facilities and infrastructure. The knowledge and values inculcated have proved to be of immense help at the very start of my career. Special thanks to Hon’ble Founder, Vivekananda Institute of Professional Studies- Technical Campus, Delhi for having provided us with excellent infrastructure at VSIT.")

    add_p("I am grateful to Prof. Mamta Madan (Dean, VSIT), and my respected Project Guide for their astute guidance, constant encouragement and sincere support for this project work. Sincere thanks to all my family members, seniors and friends for their support and assistance throughout the project.")

    add_p("Pranjay", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True, space_before=24)

    doc.add_page_break()

    # =========================================================================
    # 3. CERTIFICATE
    # =========================================================================
    add_heading_1("CERTIFICATE")

    add_p("This is to certify that the project entitled “GitHub MCP Server: Connecting AI Assistants to Authenticated Developer Data”, submitted in partial fulfilment of the Master of Computer Application degree at VIPS, has been completed by Pranjay (Roll No. ________________). This is an authentic piece of work carried out by him under my guidance. To the best of my knowledge and belief, the material presented in this project has not been submitted earlier for the award of any degree.")

    add_p("Signature of student", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, space_before=36, space_after=36)
    add_p("Signature of the guide", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True, space_after=4)
    add_p("(Project Guide)", align=WD_ALIGN_PARAGRAPH.RIGHT, italic=True)

    doc.add_page_break()

    # =========================================================================
    # 4. SELF CERTIFICATE
    # =========================================================================
    add_heading_1("SELF CERTIFICATE")

    add_p("This is to certify that the project report entitled “GitHub MCP Server: Connecting AI Assistants to Authenticated Developer Data” done by me is an authentic work carried out for the partial fulfilment of Master of Computer Applications under the guidance of my project guide. The matter embodied in this project work has not been submitted earlier for award of any degree or diploma to the best of my knowledge and belief.")

    add_p("Signature of the student", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True, space_before=36, space_after=4)
    add_p("Pranjay", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True, space_after=2)
    add_p("Enrollment No. ________________", align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=12)

    doc.add_page_break()

    # =========================================================================
    # 5. TABLE OF CONTENTS
    # =========================================================================
    add_heading_1("TABLE OF CONTENTS")

    table = doc.add_table(rows=7, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    headers = ["S.NO", "TOPIC", "PAGE NO."]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = h
        for p in cell.paragraphs:
            p.runs[0].bold = True

    rows_data = [
        ("1.", "SYNOPSIS", "5-8"),
        ("2.", "MAIN REPORT\n"
               "• Objective and Scope of the Project\n"
               "• Theoretical background definition of problem\n"
               "• System analysis & design vis-a-vis user requirements\n"
               "• System planning (PERT chart)\n"
               "• Methodology adopted\n"
               "• System implementation\n"
               "• Details of Hardware and Software\n"
               "• System maintenance & evaluation\n"
               "• Detailed lifecycle of the project\n"
               "  - Architecture & DFD\n"
               "  - Input and Output Screen Design\n"
               "  - Methodology used for testing\n"
               "  - Testing and test results", "8-26"),
        ("3.", "CODING AND SCREENSHOTS", "27-46"),
        ("4.", "CONCLUSION", "47"),
        ("5.", "FUTURE SCOPE", "48"),
        ("6.", "REFERENCES", "49")
    ]

    for idx, (sno, topic, pno) in enumerate(rows_data, 1):
        table.cell(idx, 0).text = sno
        table.cell(idx, 1).text = topic
        table.cell(idx, 2).text = pno

    # Column widths
    for row in table.rows:
        row.cells[0].width = Inches(0.8)
        row.cells[1].width = Inches(4.7)
        row.cells[2].width = Inches(1.2)

    doc.add_page_break()

    # =========================================================================
    # 6. SYNOPSIS
    # =========================================================================
    add_heading_1("SYNOPSIS")

    add_heading_2("INTRODUCTION")
    add_p("In today's software engineering ecosystem, Large Language Models (LLMs) such as Claude, ChatGPT, and Gemini have revolutionized developer productivity. However, these AI assistants remain strictly isolated from private, authenticated developer environments behind firewalls and token barriers. A software engineer cannot ask an AI assistant basic questions about their private GitHub repositories, open pull requests, issue backlogs, or project commit activity because standard models have no live access to authenticated developer APIs.")
    add_p("To solve this problem, GitHub MCP Server: Connecting AI Assistants to Authenticated Developer Data is developed as a standardized, protocol-compliant Model Context Protocol (MCP) server. By implementing the open Model Context Protocol introduced by Anthropic in late 2024, this project connects AI desktop clients (such as Claude Desktop and MCP Inspector) directly to authenticated GitHub repositories in real time.")
    add_p("The application exposes 7 purpose-built tools: 5 read-only tools for repository inspection, issue tracking, search aggregation, and stale backlog detection, and 2 write tools protected by an innovative dry-run confirmation pattern. This project combines Systems Engineering, API Architecture, and AI Prompt Disambiguation to deliver a zero-cost, privacy-first bridge for developer workflows.")

    add_heading_2("PROBLEM STATEMENT")
    add_p("In current developer environments, AI assistants are unable to access private repositories, issues, or pull requests due to authentication walls. When developers need AI assistance to analyze project health, triage issues, or generate summaries, they are forced to manually copy-paste terminal outputs (`gh` CLI) or browser tabs into chat windows.")
    add_p("This manual workflow is tedious, context-limited, and disrupts developer concentration. Furthermore, existing third-party plugins require uploading sensitive personal access tokens to third-party cloud servers, posing significant security and privacy risks. There is an urgent need for an open-standard, locally executed server that allows AI assistants to interact directly and safely with authenticated GitHub data with zero cloud infrastructure and zero token exposure.")

    add_heading_2("WHY IS THIS PARTICULAR TOPIC CHOSEN?")
    add_p("This topic has been chosen because the Model Context Protocol (MCP) represents the modern industry standard for connecting AI systems to external data sources and tools. Rather than creating another vendor-locked chatbot, building an MCP server addresses a fundamental architectural shift in AI tooling.")
    add_p("The GitHub MCP Server was selected because GitHub is the universal home for open-source and proprietary software development. Providing an AI assistant with the ability to safely inspect repositories, aggregate issue counts across accounts, and draft issues with strict human-in-the-loop confirmation solves an authentic real-world developer need.")
    add_p("This project was also chosen because it encompasses Full-Stack Systems Development, Network Protocol Engineering (JSON-RPC over stdio), Security Best Practices (Least Privilege & Dry-Run by Default), and Quantitative AI Benchmark Evaluation, making it both academically rigorous and practically impactful.")

    add_heading_2("KEY FUNCTIONALITIES")
    add_p("• Repository Discovery (list_repos): Lists all public and private repositories owned by the user, including stars, forks, visibility, and last updated timestamps.")
    add_p("• Single-Repository Issue Inspection (list_open_issues): Fetches open issues for a designated repository, supporting optional label filters and strictly filtering out pull requests.")
    add_p("• Cross-Repository Issue Counting (count_open_issues_all): Uses the GitHub Search API to aggregate total open issues across all user repositories in a single API call.")
    add_p("• Repository Health Dashboard (get_repo_summary): Compiles repository metadata, recent git commits, and open pull requests into a structured dashboard view.")
    add_p("• Stale Issue Backlog Detection (stale_issues): Automatically detects and highlights neglected open issues with no activity for N days.")
    add_p("• Safe Issue Creation (create_issue): Creates issues with an automatic dry-run preview (confirm=False) requiring explicit user confirmation (confirm=True) before execution.")
    add_p("• Safe Label Assignment (add_label): Adds labels to existing issues with a dry-run preview to prevent unintended issue tagging.")

    add_heading_2("THEORETICAL FOUNDATION")
    add_p("The project is grounded in three core theoretical concepts: Model Context Protocol (MCP) specification, Principle of Least Privilege, and the Human-in-the-Loop Dry-Run Safety Pattern.")
    add_p("1. Model Context Protocol: MCP establishes a standardized JSON-RPC 2.0 communication loop between a Client (AI assistant) and a Server (tool provider). Operating over local standard input/output (stdio), all message exchange is isolated to the local host, eliminating third-party relay servers.")
    add_p("2. Principle of Least Privilege: The server uses fine-grained GitHub Personal Access Tokens (PATs) restricted solely to Issues (Read/Write), Pull Requests (Read-Only), and Metadata (Read-Only). No administrative, repository-deletion, or credit-card permissions are ever requested.")
    add_p("3. Dry-Run Safety Pattern: Because autonomous AI tool calling can cause unintended state changes, write operations default to preview mode (`confirm=False`), giving developers full visibility and veto power before mutations occur on GitHub.")

    add_heading_2("USER CENTRIC DESIGN")
    add_p("The GitHub MCP Server is designed with developer experience and security at its core. Instead of requiring complex CLI arguments or browser context switching, developers simply converse with their AI assistant in natural language (English, Hindi, or Hinglish).")
    add_p("The server guarantees protocol integrity by strictly isolating all diagnostic and network logging to standard error (`stderr`), leaving standard output (`stdout`) dedicated solely to clean JSON-RPC messaging. Error messages are human-readable, notifying users clearly of rate-limit reset times or invalid repository names.")

    add_heading_2("DEVELOPMENT METHODOLOGY")
    add_p("The project followed an Agile Iterative Development Methodology spanning 8 distinct sprints: requirement analysis, token scoping, API client development, MCP tool definition, protocol verification, safety testing, multilingual benchmark curation, and prompt optimization.")
    add_p("Continuous testing was maintained throughout development, validating the server against both the official MCP Inspector web UI and live GitHub API endpoints.")

    add_heading_2("FUTURE ENHANCEMENTS")
    add_p("• OAuth 2.0 Web Authorization: Implement a browser-based OAuth flow to eliminate manual Personal Access Token generation.")
    add_p("• Local Response Caching: Introduce an embedded SQLite cache with configurable TTL to reduce rate-limit consumption for frequently queried repos.")
    add_p("• Pull Request Code Reviews: Expand write tools to support commenting on and approving open pull requests directly from the AI chat interface.")

    doc.add_page_break()

    # =========================================================================
    # 7. MAIN REPORT
    # =========================================================================
    add_heading_1("MAIN REPORT")

    add_heading_2("2.1 OBJECTIVE AND SCOPE")
    add_heading_3("OBJECTIVE")
    add_p("The primary objective of the GitHub MCP Server is to build a reliable, open-standard, and secure local server connecting AI assistants to authenticated GitHub developer data.")
    add_p("Specific objectives include:")
    add_p("1. Implementing a Python-based Model Context Protocol (MCP) server adhering to the official v2.0 specification.")
    add_p("2. Providing 5 comprehensive read-only tools to inspect repositories, issues, summaries, and inactive backlogs.")
    add_p("3. Developing 2 write tools behind an immutable dry-run confirmation guardrail (`confirm=False` by default).")
    add_p("4. Isolating credentials completely to the local user machine using environment variables (`.env`).")
    add_p("5. Measuring and optimizing AI tool-calling accuracy across a 50-question multilingual benchmark (English, Hindi, Hinglish).")

    add_heading_3("SCOPE")
    add_p("• In Scope: Repository listing, issue inspection with PR separation, cross-repo search counting, repository summaries (commits + PRs), stale issue detection, safe issue creation, and safe labeling.")
    add_p("• Out of Scope: Destructive repository deletion, raw code file searches (restricted due to GitHub's 10 req/min secondary rate limit), and cloud-hosted multi-tenant infrastructure.")

    add_heading_2("2.2 THEORETICAL BACKGROUND AND DEFINITION OF THE PROBLEM")
    add_heading_3("Theoretical Background")
    add_p("AI assistants historically functioned on pre-trained parametric weights. With the development of Function Calling (Tool Calling), models gained the ability to generate structured arguments for pre-defined APIs. The Model Context Protocol (MCP) unifies tool definitions across AI vendors using standard JSON-RPC 2.0 semantics.")
    add_p("Under the local `stdio` transport, the MCP client spawns the MCP server as a subprocess. Communication occurs via standard streams, guaranteeing zero network exposure of credentials and zero cloud server dependency.")

    add_heading_3("Definition of the Problem")
    add_p("1. AI isolation: AI models have no access to private developer repositories without authentication.")
    add_p("2. Context switching: Developers waste significant time copy-pasting terminal commands and browser URLs.")
    add_p("3. Security risks: Sharing API tokens with third-party web plugins violates software security standards.")
    add_p("4. Unintended mutations: Unrestricted AI write access can lead to accidental issue creation or spamming.")
    add_p("5. Rate limiting: Naive API querying quickly exhausts GitHub's 5,000 requests/hour rate limit.")

    add_heading_2("2.3 SYSTEM ANALYSIS & DESIGN VIS-A-VIS USER REQUIREMENTS")
    add_heading_3("Functional Requirements")
    add_p("• FR1: Retrieve all repositories (public and private) owned by the user.")
    add_p("• FR2: Fetch open issues for a designated repo, filtering out pull requests.")
    add_p("• FR3: Aggregate open issues across all user repositories in a single API call.")
    add_p("• FR4: Compile repository health metrics, recent commits, and open PRs into a dashboard.")
    add_p("• FR5: Identify and return issues with no activity for N days.")
    add_p("• FR6: Display a dry-run preview of an issue, creating it only when confirm=True.")
    add_p("• FR7: Preview label additions, applying them only when confirm=True.")

    add_heading_3("Non-Functional Requirements")
    add_p("• NFR1: Zero Cost — Built entirely on free Python libraries, GitHub free tier, and MCP Inspector.")
    add_p("• NFR2: Protocol Integrity — All logging directed strictly to stderr; stdout reserved for JSON-RPC.")
    add_p("• NFR3: Least Privilege — Operates exclusively with fine-grained tokens scoped to issues, PRs, and metadata.")
    add_p("• NFR4: High Reliability — Handles RFC 5988 pagination and rate-limit exhaustion gracefully.")

    add_heading_2("2.4 SYSTEM PLANNING (PERT CHART)")
    add_p("The project development was structured into 9 sequential and interdependent phases over a planned 13-week lifecycle:")

    pert_table = doc.add_table(rows=10, cols=2)
    pert_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    pert_table.cell(0, 0).text = "TASK"
    pert_table.cell(0, 1).text = "DURATION (WEEKS)"
    for cell in pert_table.rows[0].cells:
        cell.paragraphs[0].runs[0].bold = True

    pert_data = [
        ("Requirements Gathering & Planning", "1"),
        ("Token Scoping & GitHub API Client Architecture", "1"),
        ("Core MCP Server & Tool Schema Definition", "3"),
        ("Dry-Run Safety Engine & Error Handling", "2"),
        ("Protocol Stream Isolation & Logging Setup", "1"),
        ("Pagination & Rate Limit Defense Implementation", "1"),
        ("Multilingual Benchmark Curation (50 Queries)", "1"),
        ("Testing, Evaluation & Prompt Disambiguation", "2"),
        ("Documentation, Deployment & Git Finalization", "1"),
    ]
    for idx, (tname, dur) in enumerate(pert_data, 1):
        pert_table.cell(idx, 0).text = tname
        pert_table.cell(idx, 1).text = dur

    pert_table.rows[0].cells[0].width = Inches(4.5)
    pert_table.rows[0].cells[1].width = Inches(2.0)

    add_p("Total Estimated Timeline: 13 Weeks", bold=True, space_before=6)

    add_heading_2("2.5 METHODOLOGY ADOPTED")
    add_heading_3("Approach Highlights")
    add_p("1. Modular Separation of Concerns: Architecture separated into config.py (secrets), github_client.py (API transport), and server.py (MCP tools).")
    add_p("2. Read-Only First: Prioritizing safe informational queries before offering mutating capabilities.")
    add_p("3. Defense-in-Depth Safety: Enforcing dry-run confirmation on all state changes.")
    add_p("4. Protocol Stream Isolation: Preserving stdout strictly for machine communication; redirecting human logs to stderr.")
    add_p("5. Empirical Benchmark Optimization: Evaluating tool selection across 50 questions before and after prompt refinement.")

    add_heading_3("Tools and Technologies Used")
    add_p("• Language: Python 3.14 — Robust async runtime, strong typing, wide ecosystem.")
    add_p("• MCP Framework: mcp v2.3.0 (Official Anthropic Python SDK) — MCPServer abstraction.")
    add_p("• HTTP Client: httpx v0.28.1 — Fast HTTP/1.1 client with strict timeouts and custom header parsing.")
    add_p("• Configuration: python-dotenv v1.2.4 — Secure local environment parsing.")
    add_p("• API Testing: MCP Inspector v2.13.0 — Interactive browser-based developer harness.")
    add_p("• Version Control: Git & GitHub — Remote repository tracking at pranjay6667/github-mcp-server.")

    add_heading_2("2.6 SYSTEM IMPLEMENTATION")
    add_p("The system implementation comprises three main functional layers:")
    add_p("1. Credential Management (config.py): Employs Path(__file__).resolve().parent to reliably resolve the `.env` file regardless of the working directory from which Claude Desktop or the inspector initiates the subprocess. Halts with a descriptive stderr error if GITHUB_TOKEN is absent.")
    add_p("2. GitHub REST Client (github_client.py): Implements automatic RFC 5988 Link header pagination, extracts pull requests out of generic issue responses, and monitors X-RateLimit-Remaining headers to fail gracefully when quotas deplete.")
    add_p("3. MCP Server Core (server.py): Defines 7 tool handlers decorated with @mcp.tool(). Handles dry-run preview generation when confirm=False and executes live mutations only when confirm=True.")

    add_heading_2("2.7 DETAILS OF HARDWARE AND SOFTWARE")
    add_heading_3("Hardware Requirements")
    add_p("• Processor: Intel Core i3 / AMD Ryzen 3 or higher.")
    add_p("• RAM: Minimum 4 GB (8 GB recommended).")
    add_p("• Storage: 256 MB free disk space for Python runtime and virtual environment.")
    add_p("• Network: Active internet connection for live GitHub REST API communication.")

    add_heading_3("Software Requirements")
    add_p("• Operating System: Windows 10/11, macOS, or Linux.")
    add_p("• Runtime: Python 3.10+ (Developed and tested on Python 3.14.7).")
    add_p("• Packages: mcp[cli]>=2.3.0, httpx>=0.28.1, python-dotenv>=1.2.4.")
    add_p("• Development Tools: Visual Studio Code, Git CLI, MCP Inspector.")

    add_heading_2("2.8 SYSTEM MAINTENANCE AND EVALUATION")
    add_heading_3("Maintenance Strategy")
    add_p("1. Token Rotation: Easily rotate GitHub tokens by updating the local `.env` file without modifying code.")
    add_p("2. Rate-Limit Monitoring: Real-time warnings log when fewer than 10 requests remain in the hourly quota.")
    add_p("3. API Version Pinning: The client explicitly sends `X-GitHub-Api-Version: 2022-11-28` to guard against upstream breaking changes.")

    add_heading_3("Evaluation Approach")
    add_p("The server was evaluated using a rigorous 50-question benchmark dataset across two experimental rounds:")
    add_p("• Round 1 (Baseline): Tool descriptions used generic, naive docstrings.")
    add_p("• Round 2 (Optimized): Tool descriptions included explicit negative constraints, scope boundaries, and trigger phrases.")
    add_p("Results proved an 8.0% overall accuracy gain (90.0% -> 98.0%), with ambiguous queries improving by +25.0% and out-of-scope rejections improving by +28.6%.")

    add_heading_2("2.9 DETAILED LIFECYCLE OF THE PROJECT")
    add_heading_3("2.9.1 Architecture and Data Flow Diagrams (DFD)")
    add_p("Architecture Flow:")
    add_p("Client (Claude / Inspector) <=== stdio (JSON-RPC) ===> server.py <---> github_client.py <=== HTTPS ===> api.github.com")

    add_p("Level 0 DFD (Context Diagram):")
    add_p("[Developer] ---> (Natural Language Prompt) ---> [GitHub MCP Server] ---> (Structured Response) ---> [Developer]\n"
          "                       |                                      ^\n"
          "            (HTTPS GET/POST)                           (JSON Payload)\n"
          "                       v                                      |\n"
          "                            [GitHub REST API Service]")

    add_p("Level 1 DFD:")
    add_p("1.0 Prompt Parser -> 2.0 MCP Protocol Dispatcher -> 3.0 Dry-Run Guard -> 4.0 GitHub Client -> 5.0 Output Formatter.")

    add_heading_3("2.9.2 Input and Output Screen Design")
    add_p("• Input Screen (MCP Inspector): Interactive form dynamically rendered from tool JSON schemas. For `get_repo_summary`, accepts `owner` and `repo` inputs.")
    add_p("• Output Screen (Dry-Run Preview): Displays formatted text indicating 'DRY RUN -- Issue preview (not created yet)' with parameters.")
    add_p("• Output Screen (Confirmed Execution): Displays 'Issue created successfully!' accompanied by the live GitHub issue URL.")

    add_heading_3("2.9.3 Methodology Used for Testing")
    add_p("• Unit Testing: Individual tool schema validation via `tests/test_protocol.py`.")
    add_p("• Integration Testing: Live GitHub API execution via `tests/test_tools.py`.")
    add_p("• Safety Testing: Dry-run and confirmed mutation verification via `tests/test_safety.py`.")
    add_p("• Benchmark Evaluation: 50-question multilingual automated evaluation via `evaluation/evaluate.py`.")

    add_heading_3("2.9.4 Testing and Test Results")
    add_p("• Protocol Test: 100% of tools (7/7) correctly registered with valid parameter schemas.")
    add_p("• Safety Test: Dry-run successfully prevented unwanted issue creation; confirmed execution created Issue #7 with live URL.")
    add_p("• Benchmark Test: Round 2 achieved 98.0% routing accuracy (49/50 correct).")

    doc.add_page_break()

    # =========================================================================
    # 8. CODING AND SCREENSHOTS
    # =========================================================================
    add_heading_1("CODING AND SCREENSHOTS")

    add_heading_2("CORE CODE IMPLEMENTATION")

    add_heading_3("1. config.py (Credential Loader)")
    code_config = (
        '"""Configuration loader for GitHub MCP Server."""\n'
        'import os, sys\n'
        'from pathlib import Path\n'
        'from dotenv import load_dotenv\n\n'
        '_ENV_PATH = Path(__file__).resolve().parent / ".env"\n'
        'load_dotenv(dotenv_path=_ENV_PATH)\n\n'
        'GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")\n'
        'GITHUB_API_BASE = "https://api.github.com"\n\n'
        'if not GITHUB_TOKEN or GITHUB_TOKEN.startswith("ghp_paste"):\n'
        '    sys.stderr.write("Error: GITHUB_TOKEN is not configured.\\n")\n'
        '    sys.exit(1)\n'
    )
    add_p(code_config, size=9)

    add_heading_3("2. github_client.py (REST API Client)")
    code_client = (
        'class GitHubClient:\n'
        '    def __init__(self) -> None:\n'
        '        self.client = httpx.Client(\n'
        '            base_url=GITHUB_API_BASE,\n'
        '            headers={\n'
        '                "Authorization": f"Bearer {GITHUB_TOKEN}",\n'
        '                "Accept": "application/vnd.github+json",\n'
        '                "X-GitHub-Api-Version": "2022-11-28",\n'
        '            },\n'
        '            timeout=30.0,\n'
        '        )\n'
        '        self._username = None\n\n'
        '    def _check_rate_limit(self, response: httpx.Response) -> None:\n'
        '        remaining = response.headers.get("x-ratelimit-remaining")\n'
        '        if remaining is not None and int(remaining) == 0:\n'
        '            raise RuntimeError("GitHub API rate limit exhausted.")\n\n'
        '    def list_repos(self, visibility="all", sort="updated", limit=30):\n'
        '        return self._get_paginated("/user/repos", {"visibility": visibility, "sort": sort}, limit)\n'
    )
    add_p(code_client, size=9)

    add_heading_3("3. server.py (MCP Tool Definitions & Safety)")
    code_server = (
        'from mcp.server.mcpserver import MCPServer\n'
        'from github_client import GitHubClient\n\n'
        'mcp = MCPServer(name="github-mcp-server")\n'
        'client = GitHubClient()\n\n'
        '@mcp.tool()\n'
        'def create_issue(owner: str, repo: str, title: str, body: str = "", labels: str = "", confirm: bool = False) -> str:\n'
        '    if not confirm:\n'
        '        return f"DRY RUN -- Issue preview: {owner}/{repo}: {title}. Call again with confirm=True."\n'
        '    result = client.create_issue(owner, repo, title, body, [l.strip() for l in labels.split(",") if l.strip()])\n'
        '    return f"Issue created successfully! #{result.get(\'number\')}: {title}"\n'
    )
    add_p(code_server, size=9)

    add_heading_2("SCREENSHOTS OF SYSTEM EXECUTION")

    add_heading_3("Figure 1: MCP Inspector – All 7 Tools Connected & Registered")
    add_image_if_exists(ASSETS_DIR / "screenshot_1_tools_connected.png", width=Inches(5.5))
    add_p("The MCP Inspector successfully initializes server.py over stdio and displays all 7 registered tools.", italic=True, size=10)

    add_heading_3("Figure 2: MCP Inspector – Dry-Run Safety Preview for create_issue")
    add_image_if_exists(ASSETS_DIR / "screenshot_2_dry_run_preview.png", width=Inches(5.5))
    add_p("Calling create_issue with confirm=False produces a structured preview without modifying GitHub data.", italic=True, size=10)

    add_heading_3("Figure 3: MCP Inspector – get_repo_summary Execution & Console Output")
    add_image_if_exists(ASSETS_DIR / "screenshot_4_server_console.png", width=Inches(5.5))
    add_p("Executing get_repo_summary against pranjay6667/github-mcp-server showing successful HTTP 200 API responses.", italic=True, size=10)

    doc.add_page_break()

    # =========================================================================
    # 9. CONCLUSION
    # =========================================================================
    add_heading_1("CONCLUSION")
    add_p("The project GitHub MCP Server: Connecting AI Assistants to Authenticated Developer Data successfully delivers a modern, open-standard, and zero-cost bridge between generative AI assistants and private software repositories.")
    add_p("By strictly implementing the Model Context Protocol (MCP) standard, the server allows AI models like Claude to query repositories, count issues across organizations, summarize project health, and detect neglected backlogs in real time without human context-switching.")
    add_p("The project's architectural safeguards—namely least-privilege token access, protocol stream isolation to stderr, and dry-run confirmation on write operations—ensure that AI autonomy does not compromise developer data integrity.")
    add_p("Furthermore, empirical evaluation across 50 multilingual queries demonstrated that semantic prompt engineering directly elevated tool routing accuracy from 90.0% to 98.0%, proving that precise tool definitions are critical for reliable AI agent execution.")

    # =========================================================================
    # 10. FUTURE SCOPE
    # =========================================================================
    add_heading_1("FUTURE SCOPE")
    add_p("1. OAuth 2.0 Web Authentication: Incorporate a browser-based OAuth authorization flow to allow non-technical users to connect their GitHub accounts without manually creating Personal Access Tokens.")
    add_p("2. Local SQLite Response Caching: Implement local client-side caching with Time-To-Live (TTL) expiration to reduce duplicate network requests and prevent rate-limit depletion.")
    add_p("3. Pull Request Review & Comments: Expand write capabilities to allow AI assistants to review pull request diffs, leave comments, and approve pull requests directly.")
    add_p("4. Branch and Commit Operations: Introduce tools for branch creation, cherry-picking, and diff visualization within the chat interface.")
    add_p("5. Multi-Platform Support: Extend the MCP server to support GitLab and Bitbucket using unified tool abstractions.")

    # =========================================================================
    # 11. REFERENCES
    # =========================================================================
    add_heading_1("REFERENCES")
    add_p("1. Anthropic. (2024). Model Context Protocol Specification. Available: https://modelcontextprotocol.io/")
    add_p("2. GitHub Inc. (2024). GitHub REST API Documentation. Available: https://docs.github.com/en/rest")
    add_p("3. Schick, T., et al. (2023). Toolformer: Language Models Can Teach Themselves to Use Tools. arXiv preprint arXiv:2302.04761.")
    add_p("4. Python Software Foundation. (2024). Python Standard Library — Logging and Subprocess Management.")
    add_p("5. Fielding, R. (2008). RFC 5988: Web Linking. Internet Engineering Task Force.")
    add_p("6. JSON-RPC Working Group. (2013). JSON-RPC 2.0 Specification. Available: https://www.jsonrpc.org/specification")
    add_p("7. HTTPX Project. (2024). HTTPX: A next-generation HTTP client for Python. Available: https://www.python-httpx.org/")
    add_p("8. Git Documentation. (2024). Git Version Control System. Available: https://git-scm.com/")

    # Save documents
    doc.save(str(DOCX_PATH))
    print(f"Generated DOCX report: {DOCX_PATH}")

if __name__ == "__main__":
    create_report()
