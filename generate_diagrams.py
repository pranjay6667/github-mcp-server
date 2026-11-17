"""
Generates all high-resolution engineering diagrams for the VIPS-TC / GGSIPU Project Report:
1. PERT / Gantt Chart (13 Weeks)
2. System Architecture Diagram
3. DFD Level 0 (Context Diagram)
4. DFD Level 1 (Process Breakdown)
5. ER Diagram (Data Entities & Relationships)
6. Flowchart - Read Request Pipeline
7. Flowchart - Write Safety & Dry-Run Pipeline
8. Evaluation Benchmark Results Chart
"""

import os
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

OUTPUT_DIR = Path(r"C:\Users\pranj\.gemini\antigravity\scratch\github-mcp-server\docs\assets")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# -----------------------------------------------------------------------------
# 1. PERT / GANTT CHART
# -----------------------------------------------------------------------------
def generate_pert_chart():
    fig, ax = plt.subplots(figsize=(11, 6), dpi=300)
    tasks = [
        "1. Requirements Gathering & Problem Analysis",
        "2. Token Scoping & API Architecture",
        "3. Core MCP Server (server.py)",
        "4. REST Client Development (github_client.py)",
        "5. Dry-Run Safety Engine (Write Tools)",
        "6. Protocol Stream Isolation & Stderr Logging",
        "7. Pagination & Rate-Limit Defense",
        "8. Multilingual Benchmark Curation (50 Queries)",
        "9. Testing, Prompt Disambiguation & Evaluation",
        "10. Documentation, Deployment & Git Finalization",
    ]
    starts = [0, 1, 2, 2, 5, 7, 8, 9, 10, 12]
    durations = [1, 1, 3, 3, 2, 1, 1, 1, 2, 1]
    colors = [
        "#F59E0B", "#F97316", "#10B981", "#059669",
        "#8B5CF6", "#6366F1", "#06B6D4", "#EC4899",
        "#D97706", "#2563EB"
    ]

    y_pos = np.arange(len(tasks))
    ax.barh(y_pos, durations, left=starts, align='center', height=0.55, color=colors, edgecolor='#1E293B', linewidth=1)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(tasks, fontsize=9.5, fontweight='bold', color='#1E293B')
    ax.invert_yaxis()
    ax.set_xlabel("Project Timeline (Weeks)", fontsize=11, fontweight='bold', labelpad=8)
    ax.set_xlim(0, 13)
    ax.set_xticks(range(14))
    ax.set_xticklabels([f"W{i}" if i > 0 else "Start" for i in range(14)], fontsize=9, fontweight='bold')
    ax.grid(axis='x', linestyle='--', alpha=0.6, color='#94A3B8')

    for i, (s, d) in enumerate(zip(starts, durations)):
        ax.text(s + d / 2, i, f"{d}w", va='center', ha='center', color='white', fontweight='bold', fontsize=8.5)

    ax.set_title("GitHub MCP Server – Project Planning (Gantt / PERT Schedule: 13 Weeks)", fontsize=13, fontweight='bold', pad=14, color='#0F172A')
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "diagram_pert_chart.png")
    plt.close(fig)
    print("Generated diagram_pert_chart.png")

# -----------------------------------------------------------------------------
# 2. SYSTEM ARCHITECTURE
# -----------------------------------------------------------------------------
def generate_architecture():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Background container for Local Host
    local_box = patches.FancyBboxPatch((0.5, 0.5), 6.2, 4.8, boxstyle="round,pad=0.2", fc="#F8FAFC", ec="#64748B", lw=2, linestyle='--')
    ax.add_patch(local_box)
    ax.text(3.6, 5.0, "LOCAL HOST / USER ENVIRONMENT", ha='center', va='center', fontsize=11, fontweight='bold', color='#475569')

    # Client Box
    client_box = patches.FancyBboxPatch((0.8, 2.0), 2.2, 2.0, boxstyle="round,pad=0.15", fc="#EFF6FF", ec="#2563EB", lw=2)
    ax.add_patch(client_box)
    ax.text(1.9, 3.4, "MCP Client", ha='center', va='center', fontsize=11, fontweight='bold', color='#1E40AF')
    ax.text(1.9, 2.8, "• Claude Desktop\n• MCP Inspector\n• IDE Plugin", ha='center', va='center', fontsize=8.5, color='#1E3A8A')

    # Server Box
    server_box = patches.FancyBboxPatch((4.2, 1.2), 2.2, 3.2, boxstyle="round,pad=0.15", fc="#F0FDF4", ec="#16A34A", lw=2)
    ax.add_patch(server_box)
    ax.text(5.3, 4.0, "GitHub MCP Server", ha='center', va='center', fontsize=10.5, fontweight='bold', color='#166534')
    ax.text(5.3, 3.5, "server.py", ha='center', va='center', fontsize=9, fontweight='bold', color='#047857')
    ax.text(5.3, 2.8, "7 Tool Definitions\nSchema Validation\nDry-Run Engine", ha='center', va='center', fontsize=8, color='#065F46')
    ax.text(5.3, 1.8, "github_client.py\nPagination & Rate Limits", ha='center', va='center', fontsize=8, color='#065F46')

    # Config Box
    cfg_box = patches.FancyBboxPatch((4.4, 0.6), 1.8, 0.5, boxstyle="round,pad=0.08", fc="#FEF3C7", ec="#D97706", lw=1.5)
    ax.add_patch(cfg_box)
    ax.text(5.3, 0.85, "config.py (.env token)", ha='center', va='center', fontsize=8, fontweight='bold', color='#92400E')

    # External GitHub API Box
    api_box = patches.FancyBboxPatch((7.6, 1.8), 2.0, 2.4, boxstyle="round,pad=0.15", fc="#FAF5FF", ec="#9333EA", lw=2)
    ax.add_patch(api_box)
    ax.text(8.6, 3.5, "GitHub REST API", ha='center', va='center', fontsize=11, fontweight='bold', color='#6B21A8')
    ax.text(8.6, 2.9, "api.github.com\n\n• /user/repos\n• /repos/.../issues\n• /search/issues", ha='center', va='center', fontsize=8, color='#581C87')

    # Arrows
    # Client <-> Server
    ax.annotate('', xy=(4.2, 3.0), xytext=(3.0, 3.0),
                arrowprops=dict(arrowstyle="<->", lw=2.5, color="#2563EB"))
    ax.text(3.6, 3.3, "stdio\nJSON-RPC 2.0", ha='center', va='center', fontsize=8, fontweight='bold', color='#1E40AF')

    # Server <-> GitHub
    ax.annotate('', xy=(7.6, 3.0), xytext=(6.4, 3.0),
                arrowprops=dict(arrowstyle="<->", lw=2.5, color="#9333EA"))
    ax.text(7.0, 3.3, "HTTPS\nBearer Auth", ha='center', va='center', fontsize=8, fontweight='bold', color='#6B21A8')

    ax.set_title("GitHub MCP Server – High-Level System Architecture Diagram", fontsize=12.5, fontweight='bold', pad=12, color='#0F172A')
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "diagram_architecture.png")
    plt.close(fig)
    print("Generated diagram_architecture.png")

# -----------------------------------------------------------------------------
# 3. DFD LEVEL 0 (Context Diagram)
# -----------------------------------------------------------------------------
def generate_dfd_level_0():
    fig, ax = plt.subplots(figsize=(9, 4.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')

    # Entity: Developer / User
    user_box = patches.FancyBboxPatch((0.5, 1.8), 2.2, 1.4, boxstyle="round,pad=0.1", fc="#EFF6FF", ec="#1D4ED8", lw=2)
    ax.add_patch(user_box)
    ax.text(1.6, 2.7, "DEVELOPER / AI CLIENT", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1E40AF')
    ax.text(1.6, 2.2, "(Claude Desktop / Inspector)", ha='center', va='center', fontsize=8, color='#1E3A8A')

    # Process 0: GitHub MCP Server
    proc_circle = patches.Circle((5.0, 2.5), 1.25, fc="#F0FDF4", ec="#15803D", lw=2.5)
    ax.add_patch(proc_circle)
    ax.text(5.0, 2.7, "0", ha='center', va='center', fontsize=14, fontweight='bold', color='#166534')
    ax.text(5.0, 2.3, "GITHUB MCP\nSERVER SYSTEM", ha='center', va='center', fontsize=9, fontweight='bold', color='#14532D')

    # Entity: GitHub API
    api_box = patches.FancyBboxPatch((7.3, 1.8), 2.2, 1.4, boxstyle="round,pad=0.1", fc="#FAF5FF", ec="#7E22CE", lw=2)
    ax.add_patch(api_box)
    ax.text(8.4, 2.7, "GITHUB REST API", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#6B21A8')
    ax.text(8.4, 2.2, "(api.github.com)", ha='center', va='center', fontsize=8, color='#581C87')

    # Arrows between User and Process 0
    ax.annotate('', xy=(3.75, 2.8), xytext=(2.7, 2.8),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#1D4ED8"))
    ax.text(3.2, 3.1, "Natural Language\nPrompt / Tool Call", ha='center', va='center', fontsize=7.5, color='#1E40AF')

    ax.annotate('', xy=(2.7, 2.1), xytext=(3.75, 2.1),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#059669"))
    ax.text(3.2, 1.7, "Structured Output /\nDry-Run Preview", ha='center', va='center', fontsize=7.5, color='#047857')

    # Arrows between Process 0 and GitHub API
    ax.annotate('', xy=(7.3, 2.8), xytext=(6.25, 2.8),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#7E22CE"))
    ax.text(6.8, 3.1, "Authenticated HTTPS\nRequests (GET / POST)", ha='center', va='center', fontsize=7.5, color='#6B21A8')

    ax.annotate('', xy=(6.25, 2.1), xytext=(7.3, 2.1),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#D97706"))
    ax.text(6.8, 1.7, "JSON Response Data\n& Pagination Headers", ha='center', va='center', fontsize=7.5, color='#B45309')

    ax.set_title("Data Flow Diagram – Level 0 (Context Diagram)", fontsize=12.5, fontweight='bold', pad=10, color='#0F172A')
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "diagram_dfd_level_0.png")
    plt.close(fig)
    print("Generated diagram_dfd_level_0.png")

# -----------------------------------------------------------------------------
# 4. DFD LEVEL 1 (Process Decomposition)
# -----------------------------------------------------------------------------
def generate_dfd_level_1():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Processes
    p1 = patches.Circle((1.5, 3.8), 0.75, fc="#EFF6FF", ec="#2563EB", lw=2)
    ax.add_patch(p1)
    ax.text(1.5, 4.0, "1.0", ha='center', va='center', fontsize=10, fontweight='bold', color='#1E40AF')
    ax.text(1.5, 3.6, "Prompt Parser\n& Tool Select", ha='center', va='center', fontsize=7, color='#1E3A8A')

    p2 = patches.Circle((4.0, 3.8), 0.75, fc="#F5F3FF", ec="#7C3AED", lw=2)
    ax.add_patch(p2)
    ax.text(4.0, 4.0, "2.0", ha='center', va='center', fontsize=10, fontweight='bold', color='#5B21B6')
    ax.text(4.0, 3.6, "Parameter\nValidation", ha='center', va='center', fontsize=7, color='#4C1D95')

    p3 = patches.Circle((6.5, 3.8), 0.75, fc="#FEF3C7", ec="#D97706", lw=2)
    ax.add_patch(p3)
    ax.text(6.5, 4.0, "3.0", ha='center', va='center', fontsize=10, fontweight='bold', color='#92400E')
    ax.text(6.5, 3.6, "Dry-Run Safety\nGuardrail", ha='center', va='center', fontsize=7, color='#78350F')

    p4 = patches.Circle((6.5, 1.5), 0.75, fc="#F0FDF4", ec="#16A34A", lw=2)
    ax.add_patch(p4)
    ax.text(6.5, 1.7, "4.0", ha='center', va='center', fontsize=10, fontweight='bold', color='#166534')
    ax.text(6.5, 1.3, "GitHub API\nClient Engine", ha='center', va='center', fontsize=7, color='#14532D')

    p5 = patches.Circle((2.5, 1.5), 0.75, fc="#ECFDF5", ec="#059669", lw=2)
    ax.add_patch(p5)
    ax.text(2.5, 1.7, "5.0", ha='center', va='center', fontsize=10, fontweight='bold', color='#065F46')
    ax.text(2.5, 1.3, "Response\nFormatter", ha='center', va='center', fontsize=7, color='#047857')

    # Data Store D1: .env config
    d1_box = patches.FancyBboxPatch((8.3, 3.4), 1.5, 0.8, boxstyle="square,pad=0.05", fc="#FEF2F2", ec="#DC2626", lw=1.5)
    ax.add_patch(d1_box)
    ax.text(9.05, 3.9, "D1: .env Config", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#991B1B')
    ax.text(9.05, 3.6, "GITHUB_TOKEN", ha='center', va='center', fontsize=7, color='#7F1D1D')

    # Arrows
    # 1.0 -> 2.0
    ax.annotate('', xy=(3.25, 3.8), xytext=(2.25, 3.8), arrowprops=dict(arrowstyle="->", lw=1.5, color="#2563EB"))
    ax.text(2.75, 4.1, "Tool & Args", ha='center', va='center', fontsize=7)

    # 2.0 -> 3.0
    ax.annotate('', xy=(5.75, 3.8), xytext=(4.75, 3.8), arrowprops=dict(arrowstyle="->", lw=1.5, color="#7C3AED"))
    ax.text(5.25, 4.1, "Validated Call", ha='center', va='center', fontsize=7)

    # 3.0 -> User (Dry-run preview)
    ax.annotate('', xy=(1.5, 4.8), xytext=(6.5, 4.55), arrowprops=dict(arrowstyle="->", lw=1.5, color="#D97706", connectionstyle="arc3,rad=-0.3"))
    ax.text(4.0, 5.2, "Dry-Run Preview (if confirm == False)", ha='center', va='center', fontsize=7.5, color='#B45309')

    # 3.0 -> 4.0 (If confirm == True or Read Tool)
    ax.annotate('', xy=(6.5, 2.25), xytext=(6.5, 3.05), arrowprops=dict(arrowstyle="->", lw=1.5, color="#16A34A"))
    ax.text(7.2, 2.65, "Authorized Call\n(confirm == True)", ha='center', va='center', fontsize=7)

    # D1 -> 4.0
    ax.annotate('', xy=(7.25, 1.6), xytext=(8.3, 3.4), arrowprops=dict(arrowstyle="->", lw=1.5, color="#DC2626", linestyle='--'))
    ax.text(8.2, 2.3, "Auth Token", ha='center', va='center', fontsize=7, color='#B91C1C')

    # 4.0 -> 5.0
    ax.annotate('', xy=(3.25, 1.5), xytext=(5.75, 1.5), arrowprops=dict(arrowstyle="->", lw=1.5, color="#059669"))
    ax.text(4.5, 1.8, "Raw API JSON Data", ha='center', va='center', fontsize=7)

    # 5.0 -> User Output
    ax.annotate('', xy=(0.8, 1.5), xytext=(1.75, 1.5), arrowprops=dict(arrowstyle="->", lw=2, color="#0D9488"))
    ax.text(1.2, 1.1, "Final Clean\nText to User", ha='center', va='center', fontsize=7.5, color='#0F766E')

    ax.set_title("Data Flow Diagram – Level 1 (Process Decomposition)", fontsize=12.5, fontweight='bold', pad=10, color='#0F172A')
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "diagram_dfd_level_1.png")
    plt.close(fig)
    print("Generated diagram_dfd_level_1.png")

# -----------------------------------------------------------------------------
# 5. ER DIAGRAM
# -----------------------------------------------------------------------------
def generate_erd():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    def draw_entity(x, y, w, h, title, attrs, color="#EFF6FF", border="#2563EB"):
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", fc=color, ec=border, lw=2)
        ax.add_patch(box)
        ax.text(x + w / 2, y + h - 0.25, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0F172A')
        line = patches.Rectangle((x, y + h - 0.45), w, 0.02, fc=border)
        ax.add_patch(line)
        for i, a in enumerate(attrs):
            ax.text(x + 0.15, y + h - 0.7 - (i * 0.28), a, ha='left', va='center', fontsize=7.5, color='#334155')

    draw_entity(0.6, 3.4, 2.4, 2.0, "USER / OWNER",
                ["• user_id (PK)", "• username (login)", "• token_scope", "• rate_limit_remaining", "• public_repos_count"])

    draw_entity(4.0, 3.4, 2.4, 2.1, "REPOSITORY",
                ["• repo_id (PK)", "• full_name (UQ)", "• visibility (public/priv)", "• stars_count", "• open_issues_count", "• updated_at"])

    draw_entity(7.2, 3.4, 2.3, 2.0, "PULL REQUEST",
                ["• pr_id (PK)", "• number", "• title", "• author", "• state (open)", "• repo_id (FK)"])

    draw_entity(4.0, 0.5, 2.4, 2.1, "ISSUE",
                ["• issue_id (PK)", "• number", "• title", "• body", "• author", "• days_stale", "• repo_id (FK)"])

    draw_entity(7.2, 0.5, 2.3, 1.8, "LABEL",
                ["• label_id (PK)", "• name (e.g. bug)", "• color_hex", "• description", "• issue_id (FK)"])

    draw_entity(0.6, 0.5, 2.4, 1.8, "MCP TOOL CALL",
                ["• call_id (PK)", "• tool_name", "• confirm (bool)", "• timestamp", "• status (success/preview)"])

    # Relationships
    # User -> Repo (1:N)
    ax.annotate('', xy=(4.0, 4.4), xytext=(3.0, 4.4), arrowprops=dict(arrowstyle="->", lw=1.5, color="#2563EB"))
    ax.text(3.5, 4.6, "1 : N\nowns", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#1D4ED8')

    # Repo -> Issue (1:N)
    ax.annotate('', xy=(5.2, 2.6), xytext=(5.2, 3.4), arrowprops=dict(arrowstyle="->", lw=1.5, color="#16A34A"))
    ax.text(5.5, 3.0, "1 : N\ncontains", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#15803D')

    # Repo -> PR (1:N)
    ax.annotate('', xy=(7.2, 4.4), xytext=(6.4, 4.4), arrowprops=dict(arrowstyle="->", lw=1.5, color="#7C3AED"))
    ax.text(6.8, 4.6, "1 : N\ntracks", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#6D28D9')

    # Issue -> Label (N:M)
    ax.annotate('', xy=(7.2, 1.4), xytext=(6.4, 1.4), arrowprops=dict(arrowstyle="<->", lw=1.5, color="#D97706"))
    ax.text(6.8, 1.7, "N : M\ntagged with", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#B45309')

    # Tool Call -> Issue (1:1 write preview)
    ax.annotate('', xy=(4.0, 1.4), xytext=(3.0, 1.4), arrowprops=dict(arrowstyle="->", lw=1.5, color="#059669"))
    ax.text(3.5, 1.7, "creates /\nupdates", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#047857')

    ax.set_title("Entity Relationship Diagram (ERD) – GitHub MCP Server Data Model", fontsize=12.5, fontweight='bold', pad=10, color='#0F172A')
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "diagram_erd.png")
    plt.close(fig)
    print("Generated diagram_erd.png")

# -----------------------------------------------------------------------------
# 6. FLOWCHART - READ REQUEST
# -----------------------------------------------------------------------------
def generate_flowchart_read():
    fig, ax = plt.subplots(figsize=(7, 6), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    def draw_box(x, y, w, h, text, fc="#EFF6FF", ec="#2563EB"):
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", fc=fc, ec=ec, lw=1.5)
        ax.add_patch(box)
        ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#0F172A')

    draw_box(3.0, 8.8, 4.0, 0.7, "User Prompt (e.g. 'Show open issues')", fc="#DBEAFE", ec="#1D4ED8")
    draw_box(3.0, 7.5, 4.0, 0.7, "LLM Dispatches Read Tool (list_open_issues)")
    draw_box(3.0, 6.2, 4.0, 0.7, "Input Bounds Validation (limit, owner, repo)")
    draw_box(3.0, 4.9, 4.0, 0.7, "Send GET Request to api.github.com")

    # Decision diamond
    diamond = patches.Polygon([[5.0, 4.2], [6.8, 3.4], [5.0, 2.6], [3.2, 3.4]], fc="#FEF3C7", ec="#D97706", lw=1.5)
    ax.add_patch(diamond)
    ax.text(5.0, 3.4, "Response\nStatus 200?", ha='center', va='center', fontsize=8, fontweight='bold')

    draw_box(6.8, 1.8, 2.8, 0.8, "Parse Link Headers &\nFilter out Pull Requests", fc="#DCFCE7", ec="#16A34A")
    draw_box(6.8, 0.4, 2.8, 0.7, "Format Markdown Output", fc="#DCFCE7", ec="#16A34A")

    draw_box(0.4, 1.8, 2.8, 0.8, "Handle Error Status\n(401 Auth / 404 Not Found /\nRate Limit Exhaustion)", fc="#FEE2E2", ec="#DC2626")

    # Arrows
    ax.annotate('', xy=(5.0, 8.2), xytext=(5.0, 8.8), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(5.0, 6.9), xytext=(5.0, 7.5), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(5.0, 5.6), xytext=(5.0, 6.2), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(5.0, 4.2), xytext=(5.0, 4.9), arrowprops=dict(arrowstyle="->", lw=1.5))

    # Yes branch
    ax.annotate('', xy=(6.8, 3.4), xytext=(8.2, 3.4), arrowprops=dict(arrowstyle="-", lw=1.5, color="#16A34A"))
    ax.annotate('', xy=(8.2, 2.6), xytext=(8.2, 3.4), arrowprops=dict(arrowstyle="->", lw=1.5, color="#16A34A"))
    ax.text(7.2, 3.6, "YES (200 OK)", fontsize=7.5, fontweight='bold', color="#16A34A")
    ax.annotate('', xy=(8.2, 1.1), xytext=(8.2, 1.8), arrowprops=dict(arrowstyle="->", lw=1.5, color="#16A34A"))

    # No branch
    ax.annotate('', xy=(3.2, 3.4), xytext=(1.8, 3.4), arrowprops=dict(arrowstyle="-", lw=1.5, color="#DC2626"))
    ax.annotate('', xy=(1.8, 2.6), xytext=(1.8, 3.4), arrowprops=dict(arrowstyle="->", lw=1.5, color="#DC2626"))
    ax.text(2.1, 3.6, "NO (Error)", fontsize=7.5, fontweight='bold', color="#DC2626")

    ax.set_title("Flowchart: Read Request & Pagination Workflow", fontsize=11.5, fontweight='bold', pad=10)
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "diagram_flowchart_read.png")
    plt.close(fig)
    print("Generated diagram_flowchart_read.png")

# -----------------------------------------------------------------------------
# 7. FLOWCHART - WRITE SAFETY & DRY-RUN
# -----------------------------------------------------------------------------
def generate_flowchart_write():
    fig, ax = plt.subplots(figsize=(7, 6.5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    def draw_box(x, y, w, h, text, fc="#EFF6FF", ec="#2563EB"):
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08", fc=fc, ec=ec, lw=1.5)
        ax.add_patch(box)
        ax.text(x + w / 2, y + h / 2, text, ha='center', va='center', fontsize=8, fontweight='bold', color='#0F172A')

    draw_box(2.8, 9.0, 4.4, 0.65, "User: 'Create issue titled Fix CSS bug'", fc="#DBEAFE", ec="#1D4ED8")
    draw_box(2.8, 7.8, 4.4, 0.65, "LLM calls create_issue(confirm=False)")
    draw_box(2.8, 6.6, 4.4, 0.65, "server.py validates title & repo parameters")

    # Decision Diamond
    diamond = patches.Polygon([[5.0, 5.8], [7.0, 4.9], [5.0, 4.0], [3.0, 4.9]], fc="#FEF3C7", ec="#D97706", lw=1.5)
    ax.add_patch(diamond)
    ax.text(5.0, 4.9, "Is confirm == True?", ha='center', va='center', fontsize=8, fontweight='bold')

    # NO branch (Dry-Run Preview)
    draw_box(0.5, 3.0, 3.4, 0.8, "Generate DRY-RUN Preview:\nRepo, Title, Body, Labels", fc="#FEF2F2", ec="#DC2626")
    draw_box(0.5, 1.4, 3.4, 0.8, "Return Preview to User with\nExplicit Prompt for Confirmation", fc="#FEF2F2", ec="#DC2626")

    # YES branch (Execution)
    draw_box(6.1, 3.0, 3.4, 0.8, "Dispatch POST Request to\napi.github.com/repos/.../issues", fc="#DCFCE7", ec="#16A34A")
    draw_box(6.1, 1.4, 3.4, 0.8, "Receive HTTP 201 Created &\nReturn Live Issue URL to User", fc="#DCFCE7", ec="#16A34A")

    # Connecting arrows
    ax.annotate('', xy=(5.0, 8.45), xytext=(5.0, 9.0), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(5.0, 7.25), xytext=(5.0, 7.8), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.annotate('', xy=(5.0, 5.8), xytext=(5.0, 6.6), arrowprops=dict(arrowstyle="->", lw=1.5))

    # NO Branch (left)
    ax.annotate('', xy=(3.0, 4.9), xytext=(2.2, 4.9), arrowprops=dict(arrowstyle="-", lw=1.5, color="#DC2626"))
    ax.annotate('', xy=(2.2, 3.8), xytext=(2.2, 4.9), arrowprops=dict(arrowstyle="->", lw=1.5, color="#DC2626"))
    ax.text(2.4, 5.1, "NO (Default)", fontsize=7.5, fontweight='bold', color="#DC2626")
    ax.annotate('', xy=(2.2, 2.2), xytext=(2.2, 3.0), arrowprops=dict(arrowstyle="->", lw=1.5, color="#DC2626"))

    # User confirmation loop
    ax.annotate('', xy=(6.5, 4.2), xytext=(2.2, 1.4),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#2563EB", connectionstyle="arc3,rad=-0.4", linestyle='--'))
    ax.text(4.4, 2.3, "User replies 'Yes, confirm' ->\nLLM calls create_issue(confirm=True)", fontsize=7.5, color="#1D4ED8", fontweight='bold', ha='center')

    # YES Branch (right)
    ax.annotate('', xy=(7.0, 4.9), xytext=(7.8, 4.9), arrowprops=dict(arrowstyle="-", lw=1.5, color="#16A34A"))
    ax.annotate('', xy=(7.8, 3.8), xytext=(7.8, 4.9), arrowprops=dict(arrowstyle="->", lw=1.5, color="#16A34A"))
    ax.text(7.2, 5.1, "YES", fontsize=7.5, fontweight='bold', color="#16A34A")
    ax.annotate('', xy=(7.8, 2.2), xytext=(7.8, 3.0), arrowprops=dict(arrowstyle="->", lw=1.5, color="#16A34A"))

    ax.set_title("Flowchart: Dry-Run Confirmation Safety Guardrail", fontsize=11.5, fontweight='bold', pad=10)
    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "diagram_flowchart_write.png")
    plt.close(fig)
    print("Generated diagram_flowchart_write.png")

# -----------------------------------------------------------------------------
# 8. BENCHMARK RESULTS CHART
# -----------------------------------------------------------------------------
def generate_benchmark_chart():
    fig, ax = plt.subplots(figsize=(8.5, 4.5), dpi=300)

    categories = ['Direct\n(20 Qs)', 'Multilingual\n(15 Qs)', 'Ambiguous\n(8 Qs)', 'Out-of-Scope\n(7 Qs)', 'Overall\n(50 Qs)']
    round1_acc = [100.0, 100.0, 62.5, 71.4, 90.0]
    round2_acc = [100.0, 100.0, 87.5, 100.0, 98.0]

    x = np.arange(len(categories))
    width = 0.35

    rects1 = ax.bar(x - width/2, round1_acc, width, label='Round 1 (Naive Docstrings)', color='#93C5FD', edgecolor='#1E40AF', lw=1.2)
    rects2 = ax.bar(x + width/2, round2_acc, width, label='Round 2 (Refined with Negative Constraints)', color='#10B981', edgecolor='#065F46', lw=1.2)

    ax.set_ylabel('Accuracy (%)', fontsize=11, fontweight='bold', labelpad=8)
    ax.set_title('Evaluation Benchmark: Tool Selection Accuracy Comparison', fontsize=12.5, fontweight='bold', pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=9.5, fontweight='bold')
    ax.set_ylim(0, 115)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.legend(frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1', fontsize=9)

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.1f}%',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8.5, fontweight='bold')

    autolabel(rects1)
    autolabel(rects2)

    plt.tight_layout()
    fig.savefig(OUTPUT_DIR / "diagram_benchmark_results.png")
    plt.close(fig)
    print("Generated diagram_benchmark_results.png")

if __name__ == "__main__":
    generate_pert_chart()
    generate_architecture()
    generate_dfd_level_0()
    generate_dfd_level_1()
    generate_erd()
    generate_flowchart_read()
    generate_flowchart_write()
    generate_benchmark_chart()
    print("All diagrams generated successfully!")
