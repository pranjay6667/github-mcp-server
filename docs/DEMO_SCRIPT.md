# 3 TO 5 MINUTE LIVE DEMO SCRIPT

**Project:** GitHub MCP Server: Connecting AI Assistants to Authenticated Developer Data  
**Student:** [Your Name] | **Course:** MCA Minor Project (VIPS-TC, GGSIPU)  
**Total Target Duration:** 3 to 5 minutes  

---

## 🛠️ Pre-Demo Setup Checklist (Do this 5 minutes before your viva)

1. **Verify your `.env` file** exists with your valid token:
   ```powershell
   cd C:\Users\pranj\.gemini\antigravity\scratch\github-mcp-server
   type .env
   ```
2. **Choose your demo environment**:
   - **Option A (Recommended — Claude Desktop)**: Ensure `claude_desktop_config.json` points to your `server.py` and restart Claude Desktop. Check that the hammer icon displays 7 tools.
   - **Option B (MCP Inspector)**: In your terminal, run:
     ```powershell
     .venv\Scripts\mcp.exe dev server.py
     ```
     This opens a clean web interface in your browser (`localhost:5173`) showing all tools with interactive input forms. Both are 100% valid for university evaluation.
3. **Open GitHub in your browser**: Have your repository `https://github.com/pranjay6667/Pranjay` open in a browser tab so you can immediately show the created issue live.

---

## ⏱️ Minute-by-Minute Speaking & Action Script

### Minute 0:00 – 0:45 | Introduction & Architecture
- **What to say:**
  > *"Good morning, respected external examiner and faculty members. Today I am presenting my minor project: a GitHub MCP Server built using Python and the official Model Context Protocol SDK.*
  > 
  > *Right now, Claude Desktop is running on my computer as an MCP client. In the background, my Python server `server.py` is running as a local subprocess. They are communicating over standard input/output (`stdio`) using JSON-RPC 2.0 messages.*
  > 
  > *Notice that my GitHub Personal Access Token is stored strictly on my local machine in `.env` and is never sent to any third-party server. Let me demonstrate how Claude can now securely query my private developer data."*

---

### Minute 0:45 – 1:30 | Step 1: Cross-Repository Backlog Aggregation
- **What to type in Claude Desktop / Inspector:**
  ```text
  How many total open issues do I have across all my GitHub repositories?
  ```
- **What happens behind the scenes:**
  - Claude recognizes this is a global query and selects `count_open_issues_all()`.
  - The server calls GitHub's Search API (`is:issue is:open author:pranjay6667`) in **one single HTTP request**.
- **What to say:**
  > *"Notice how Claude chose the tool `count_open_issues_all`. Instead of looping through every repository one by one — which would waste rate limits — our server uses the GitHub Search API to return the total count in a single round-trip. It shows 5 total open issues on my account, grouped by repository."*

---

### Minute 1:30 – 2:15 | Step 2: Single-Repo Inspection & Label Filtering
- **What to type in Claude Desktop / Inspector:**
  ```text
  Show me only the bug reports in my pranjay6667/Pranjay repository.
  ```
- **What happens behind the scenes:**
  - Claude extracts `owner="pranjay6667"`, `repo="Pranjay"`, and `label="bug"`.
  - The server invokes `list_open_issues` and filters out pull requests.
- **What to say:**
  > *"Here, Claude identified that the user specified a single repository and a label filter. Our server called `list_open_issues` with label='bug'.*
  > 
  > *A key engineering detail here is that GitHub's Issues REST API returns both issues and pull requests together. Our Python client inspects each item and filters out any item containing a `pull_request` key, returning only true issues."*

---

### Minute 2:15 – 3:00 | Step 3: Multilingual Query (Hinglish / Hindi)
- **What to type in Claude Desktop / Inspector:**
  ```text
  Pranjay repo ka summary overview do recent commits aur stars ke sath.
  ```
- **What happens behind the scenes:**
  - Claude understands the Hinglish intent and triggers `get_repo_summary(owner="pranjay6667", repo="Pranjay")`.
  - The server aggregates 3 distinct GitHub endpoints: repo details, commits, and pull requests.
- **What to say:**
  > *"To test usability, our benchmark evaluated queries in Hindi and Hinglish. Here, I typed in Hinglish: 'Pranjay repo ka summary overview do'.*
  > 
  > *The model correctly maps the semantics to the `get_repo_summary` tool. The server fetches the metadata, recent commits, and pull requests, and Claude formats it into a clean dashboard overview."*

---

### Minute 3:00 – 4:00 | Step 4: Safety Guardrail — The Dry-Run Preview
- **What to type in Claude Desktop / Inspector:**
  ```text
  Create a new issue titled 'Fix mobile viewport padding' in pranjay6667/Pranjay
  ```
- **What happens behind the scenes:**
  - Claude invokes `create_issue(owner="pranjay6667", repo="Pranjay", title="Fix mobile viewport padding", confirm=False)`.
  - Because `confirm` is `False`, the server returns a formatted **DRY RUN** preview without calling GitHub's POST endpoint.
- **What to say:**
  > *"This demonstrates our core safety architecture. In many AI agent systems, an autonomous model might accidentally write spam or unwanted records.*
  > 
  > *In our design, all mutating tools default to a dry run. The server returned a preview of the issue: the repository, title, and labels. Notice that no issue has been created on GitHub yet."*

---

### Minute 4:00 – 4:45 | Step 5: Confirmed Execution & Live Verification
- **What to type in Claude Desktop / Inspector:**
  ```text
  Yes, please create the issue now.
  ```
- **What happens behind the scenes:**
  - Claude recognizes user consent and calls `create_issue(..., confirm=True)`.
  - The server sends the `POST /repos/pranjay6667/Pranjay/issues` request and returns the created issue number and URL.
- **What to say & show:**
  > *"Once I explicitly confirm with 'Yes', Claude passes `confirm=True`. The server dispatches the HTTP POST request to GitHub and returns the live issue URL.*
  > 
  > *(Switch to browser)*
  > *If I refresh my GitHub repository in the browser right now, you can see the new issue created just seconds ago with the exact title and author.*
  > 
  > *This proves the end-to-end flow: from natural language understanding to safe, verified execution on GitHub."*

---

### Minute 4:45 – 5:00 | Conclusion
- **What to say:**
  > *"To summarize: we built an MCP server with 7 tools, implemented least-privilege security with fine-grained tokens, isolated logs to stderr, enforced a dry-run confirmation guardrail, and achieved a 98% accuracy rate on our 50-question benchmark.*
  > 
  > *Thank you. I am ready for your questions."*

---

## 🚨 Backup / Contingency Plan (If something goes wrong)

- **If internet is momentarily slow**:
  - Run the automated test script in terminal:
    ```powershell
    .venv\Scripts\python.exe test_all_tools.py
    ```
  - This demonstrates all 7 tools executing against the live API directly.
- **If rate limit is ever exhausted**:
  - Show `test_token.py` output showing remaining requests and headers.
