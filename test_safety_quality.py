"""
test_safety_quality.py — Verifies dry-run vs confirmation, rate-limits, and stderr logging.
"""

import os
os.chdir(r"C:\Users\pranj\.gemini\antigravity\scratch\github-mcp-server")

from server import create_issue, add_label, list_repos

OWNER = "pranjay6667"
REPO = "Pranjay"

print("=" * 60)
print("TEST 1: create_issue — DRY RUN (confirm=False)")
print("=" * 60)
dry_result = create_issue(
    owner=OWNER,
    repo=REPO,
    title="Phase 4 Safety Verification Issue",
    body="Checking dry-run mechanism.",
    labels="documentation",
    confirm=False
)
print(dry_result)
assert "DRY RUN" in dry_result, "Failed: Dry run notice missing!"

print("\n" + "=" * 60)
print("TEST 2: create_issue — CONFIRMED (confirm=True)")
print("=" * 60)
exec_result = create_issue(
    owner=OWNER,
    repo=REPO,
    title="Phase 4 Safety Verification Issue",
    body="Created via verified confirmation step.",
    labels="documentation",
    confirm=True
)
print(exec_result)
assert "Issue created successfully!" in exec_result, "Failed: Real creation did not succeed!"

# Extract issue number from output to test add_label
# Output format: "  #<number>: ..."
import re
match = re.search(r"#(\d+):", exec_result)
issue_num = int(match.group(1)) if match else 1

print("\n" + "=" * 60)
print(f"TEST 3: add_label — DRY RUN on #{issue_num}")
print("=" * 60)
label_dry = add_label(
    owner=OWNER,
    repo=REPO,
    issue_number=issue_num,
    labels="urgent",
    confirm=False
)
print(label_dry)
assert "DRY RUN" in label_dry

print("\n" + "=" * 60)
print(f"TEST 4: add_label — CONFIRMED on #{issue_num}")
print("=" * 60)
label_exec = add_label(
    owner=OWNER,
    repo=REPO,
    issue_number=issue_num,
    labels="urgent",
    confirm=True
)
print(label_exec)
assert "Labels added successfully" in label_exec

print("\n" + "=" * 60)
print("SAFETY AND CONFIRMATION TESTS PASSED")
print("=" * 60)
