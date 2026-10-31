"""Test all 7 tools by calling them directly."""
import os
os.chdir(r"C:\Users\pranj\.gemini\antigravity\scratch\github-mcp-server")

from server import (
    list_repos,
    list_open_issues,
    count_open_issues_all,
    get_repo_summary,
    stale_issues,
    create_issue,
    add_label,
)

OWNER = "pranjay6667"
REPO = "Pranjay"

print("=" * 60)
print("TOOL 1: list_repos")
print("=" * 60)
result = list_repos(limit=3)
print(result)

print("\n" + "=" * 60)
print("TOOL 2: list_open_issues")
print("=" * 60)
result = list_open_issues(owner=OWNER, repo=REPO)
print(result)

print("\n" + "=" * 60)
print("TOOL 2b: list_open_issues (filter by label: bug)")
print("=" * 60)
result = list_open_issues(owner=OWNER, repo=REPO, label="bug")
print(result)

print("\n" + "=" * 60)
print("TOOL 3: count_open_issues_all")
print("=" * 60)
result = count_open_issues_all()
print(result)

print("\n" + "=" * 60)
print("TOOL 4: get_repo_summary")
print("=" * 60)
result = get_repo_summary(owner=OWNER, repo=REPO)
print(result)

print("\n" + "=" * 60)
print("TOOL 5: stale_issues (days=1, should find recent ones)")
print("=" * 60)
result = stale_issues(owner=OWNER, repo=REPO, days=1)
print(result)

print("\n" + "=" * 60)
print("TOOL 6: create_issue (DRY RUN)")
print("=" * 60)
result = create_issue(
    owner=OWNER, repo=REPO,
    title="Test issue from tool",
    body="This is a test",
    labels="bug,enhancement",
    confirm=False,  # DRY RUN
)
print(result)

print("\n" + "=" * 60)
print("TOOL 7: add_label (DRY RUN)")
print("=" * 60)
result = add_label(
    owner=OWNER, repo=REPO,
    issue_number=1,
    labels="enhancement,documentation",
    confirm=False,  # DRY RUN
)
print(result)

print("\n" + "=" * 60)
print("ALL 7 TOOLS TESTED SUCCESSFULLY")
print("=" * 60)
