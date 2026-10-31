"""Protocol and schema verification for GitHub MCP Server.

Validates server initialization, tool registration, parameter schemas,
and compliance with the Model Context Protocol specification.
"""

import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import server

print("=" * 60)
print("MCP Server Protocol & Schema Verification")
print("=" * 60)

# 1. Server metadata verification
print(f"Server Name    : {server.mcp.name}")
print(f"Server Version : {getattr(server, '__version__', '1.0.0')}")
assert server.mcp.name == "github-mcp-server", "Server name mismatch"
assert hasattr(server.mcp, "instructions"), "Server instructions missing"
print("[OK] Server metadata verified.")

# 2. Tool registration verification
tools = server.mcp._tool_manager.list_tools()
tool_names = [t.name for t in tools]
expected_tools = [
    "list_repos",
    "list_open_issues",
    "count_open_issues_all",
    "get_repo_summary",
    "stale_issues",
    "create_issue",
    "add_label",
]

print(f"\nRegistered Tools ({len(tools)}/7):")
for t in tools:
    first_line = t.description.splitlines()[0] if t.description else "No description"
    print(f"  * {t.name:<24} - {first_line}")

assert len(tools) == 7, f"Expected 7 tools, found {len(tools)}"
for expected in expected_tools:
    assert expected in tool_names, f"Missing tool: {expected}"
print("[OK] All 7 tools registered.")

# 3. Schema & parameter validation
print("\nValidating tool parameter schemas:")
for t in tools:
    schema = t.parameters
    props = schema.get("properties", {})
    required = schema.get("required", [])
    print(f"  * {t.name}: {len(props)} parameters, {len(required)} required")

    # Safety checks on write tools
    if t.name in ("create_issue", "add_label"):
        assert "confirm" in props, f"Safety parameter 'confirm' missing in {t.name}"
        assert props["confirm"]["type"] == "boolean", f"'confirm' must be boolean in {t.name}"

print("[OK] Safety guardrails verified in schemas.")

print("\n" + "=" * 60)
print("PROTOCOL & SCHEMA VERIFICATION PASSED (100%)")
print("=" * 60)
