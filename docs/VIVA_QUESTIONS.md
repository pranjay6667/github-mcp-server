# 25 LIKELY VIVA QUESTIONS & ANSWERS

**Project:** GitHub MCP Server: Connecting AI Assistants to Authenticated Developer Data  
**Student:** [Your Name] | **Course:** MCA Minor Project (VIPS-TC, GGSIPU)  

---

## 🔹 Category 1: Model Context Protocol (MCP) Fundamentals

### Q1: What is the Model Context Protocol (MCP)?
**Answer:** MCP is an open standard introduced by Anthropic that allows AI assistants (like Claude) to securely connect to external tools and data sources. Think of it as a universal "USB port" for AI models — any server that speaks the MCP protocol can plug into any MCP-compatible client.

### Q2: What are the three core primitives in MCP?
**Answer:** 
1. **Tools:** Executable functions the model can call to take action (e.g., `list_repos`, `create_issue`).
2. **Resources:** Passive read-only data files or schemas the model can read for context.
3. **Prompts:** Reusable conversational prompt templates.

### Q3: What transport mechanism does your server use to talk to Claude Desktop?
**Answer:** It uses the **stdio (standard input/output)** transport. Both Claude Desktop and our Python script run locally on the same computer as sibling processes, exchanging messages formatted in **JSON-RPC 2.0** over standard pipes.

### Q4: Why can't you use standard `print()` statements in an MCP server?
**Answer:** In `stdio` transport, standard output (`stdout`) is strictly reserved for JSON-RPC protocol frames. A regular `print()` statement prints raw text to `stdout`, which corrupts the JSON-RPC packet and crashes the MCP client. All our server logging is redirected to `sys.stderr`.

### Q5: What is the difference between MCP SDK v1 and v2 in Python?
**Answer:** In v1, the main server class was named `FastMCP`. In SDK v2 (version 2.3.0), it was renamed to `MCPServer`. The core decorator `@mcp.tool()` and `mcp.run()` remained identical.

---

## 🔹 Category 2: Tool Calling & AI Model Interaction

### Q6: How does the AI model know which tool to call?
**Answer:** When the MCP server starts, it sends a schema containing tool names, docstrings, and parameter types to Claude. When a user asks a question, Claude reads the tool descriptions, matches the user's intent to the best tool, extracts parameter values from the query, and emits a structured tool-call request.

### Q7: Does the AI model execute your Python code directly?
**Answer:** No. The AI model only generates a text/JSON instruction indicating *which* tool to run and with *what arguments*. The local MCP server runtime receives this instruction, runs the actual Python function on your computer, and returns the string output back to the model.

### Q8: How did you handle multilingual queries (Hindi and Hinglish)?
**Answer:** Modern foundation models have cross-lingual semantic understanding. When a user asks *"Pranjay repo ke bugs dikhao"*, the model maps the intent internally to the English schema parameters (`repo="Pranjay"`, `label="bug"`). This enabled 100% accuracy on our multilingual test cases without changing our Python code.

### Q9: Why did some queries fail in Round 1 of your evaluation?
**Answer:** In Round 1, tool descriptions were too brief. For example, `count_open_issues_all` was described simply as *"Count issues"*. When users asked *"How many issues in repo X?"*, the model matched the keyword "count" instead of choosing `list_open_issues`. Adding negative boundaries in Round 2 resolved this.

---

## 🔹 Category 3: GitHub REST API & Networking

### Q10: How does GitHub's REST API handle pagination?
**Answer:** GitHub returns a maximum of 100 items per page and includes an RFC 5988 `Link` HTTP header in the response containing URLs for `rel="next"` and `rel="last"`. Our `GitHubClient._get_paginated()` helper parses this header to automatically traverse pages until the requested limit is reached.

### Q11: What is the common "gotcha" with GitHub's Issues endpoint?
**Answer:** GitHub treats Pull Requests as issues internally. When calling `GET /repos/{owner}/{repo}/issues`, GitHub returns both regular issues and PRs together. Our code checks each returned JSON object and filters out any item containing the `"pull_request"` key.

### Q12: Why did you use the Search API for `count_open_issues_all` instead of looping through repositories?
**Answer:** If a user has 20 repositories, looping through them would require 20 separate HTTP requests, which is slow and wastes API quota. The Search API (`GET /search/issues?q=is:issue is:open author:{username}`) returns the global issue count across all repositories in **one single HTTP call**.

### Q13: What rate limits does GitHub impose, and how does your server handle them?
**Answer:** For authenticated users, GitHub allows 5,000 requests per hour for the REST API and 30 requests per minute for the Search API. Our client checks `X-RateLimit-Remaining` on every response; if remaining quota drops below 10, it warns via stderr; if exhausted, it computes the reset time from `X-RateLimit-Reset` and alerts the user cleanly.

### Q14: How does `stale_issues` identify neglected issues?
**Answer:** It requests open issues sorted by `updated` ascending (oldest activity first). It parses each issue's `updated_at` ISO-8601 timestamp, compares it against the current UTC date, and checks if inactivity exceeds $N$ days. Because results are sorted oldest-first, it terminates early as soon as it encounters an active issue.

---

## 🔹 Category 4: Architecture, Security & Safety

### Q15: Why did you adopt a "Read-Only First" design?
**Answer:** To prioritize security and data safety. 5 out of our 7 tools only inspect data and cannot modify or delete anything. This allows developers to query their GitHub repositories freely without any risk of accidental repository corruption.

### Q16: How does the "Dry-Run Confirmation" pattern work in write tools?
**Answer:** In `create_issue` and `add_label`, the `confirm` parameter defaults to `False`. When called, the tool returns a preview of what *would* happen (title, repo, labels) without calling GitHub's POST endpoint. The action is only dispatched to GitHub when the user explicitly confirms and `confirm=True` is passed.

### Q17: Why did you deliberately exclude "delete" operations?
**Answer:** Autonomous AI models can misunderstand user intent or hallucinate. Providing destructive tools like `delete_repo` or `delete_issue` carries an unacceptable risk of catastrophic data loss. Deleting code should always remain a manual human operation.

### Q18: What is the Principle of Least Privilege, and how is it applied here?
**Answer:** Least privilege means granting a system only the minimum permissions necessary to perform its intended job. Instead of a classic admin Personal Access Token, we use a fine-grained token scoped strictly to `Issues (Read/Write)`, `Pull Requests (Read-Only)`, and `Metadata (Read-Only)`.

### Q19: Where are credentials stored, and how are they protected from Git leaks?
**Answer:** The GitHub token is stored in a local `.env` file and loaded into memory using `python-dotenv`. The `.env` file is explicitly listed in `.gitignore`. A template file `.env.example` with dummy values is committed instead, ensuring secrets never enter source control.

### Q20: Why did you separate `server.py`, `github_client.py`, and `config.py`?
**Answer:** To maintain clean **Separation of Concerns**:
- `config.py`: Validates environment settings and secrets at startup.
- `github_client.py`: Handles HTTP transport, headers, pagination, and error codes.
- `server.py`: Defines MCP tool schemas, docstrings, and response presentation.
If GitHub updates their API version, only `github_client.py` needs to be edited.

---

## 🔹 Category 5: Testing, Evaluation & Results

### Q21: How many questions did you evaluate, and what were the categories?
**Answer:** We evaluated **50 test questions** across 4 categories:
1. **Direct Queries (20):** Single-intent explicit commands.
2. **Multilingual Queries (15):** 9 Hinglish and 6 Hindi prompts.
3. **Ambiguous Queries (8):** Prompts where multiple tools appear relevant.
4. **Out-of-Scope Queries (7):** Prompts where no tool should trigger.

### Q22: What were your quantitative evaluation results?
**Answer:**
- **Round 1 (Naive descriptions):** 45/50 correct (**90.0% accuracy**).
- **Round 2 (Refined descriptions):** 49/50 correct (**98.0% accuracy**).
- **Overall gain:** **+8.0% overall**, with a **+25.0% gain on ambiguous queries** (62.5% -> 87.5%) and a **+28.6% gain on out-of-scope queries** (71.4% -> 100.0%).

### Q23: Give one specific example of how refining a docstring fixed an error.
**Answer:** In Round 1, the query *"How many issues are open in repo Pranjay?"* misrouted to `count_open_issues_all` because the word "count" matched the tool title. In Round 2, we added a negative constraint: *"Do NOT use when a specific repo name is mentioned; use list_open_issues instead"*. This immediately resolved the error.

### Q24: What is the financial cost of running your project?
**Answer:** **Zero cost.** The project uses Python (open-source), the free Python MCP SDK, the free GitHub REST API tier (5,000 requests/hour), and the free tier of Claude Desktop running on the user's local hardware.

### Q25: If you had another month, what two features would you add next?
**Answer:**
1. **OAuth 2.0 Web Authorization:** Allowing users to sign in with their GitHub account via a browser popup rather than manually copying and pasting a PAT token into `.env`.
2. **Local SQLite Caching:** Caching repository summaries with a 5-minute Time-To-Live (TTL) to reduce redundant network calls and save API quota.
