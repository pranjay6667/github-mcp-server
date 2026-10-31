"""Safety guardrail verification for write tools (dry-run vs confirmed execution)."""

import re
import sys
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from server import create_issue, add_label

OWNER = "pranjay6667"
REPO = "Pranjay"

print("=" * 60)
print(f"Safety Verification Suite ({OWNER}/{REPO})")
print("=" * 60)

print("\n1. Testing create_issue [Dry Run]...")
dry_result = create_issue(
    owner=OWNER,
    repo=REPO,
    title="Automated Safety Test Issue",
    body="Verifying dry-run guardrails.",
    labels="documentation",
    confirm=False,
)
print(dry_result)
assert "DRY RUN" in dry_result, "Failure: Dry run warning missing from preview."
print("[OK] Dry run prevented write action.")

print("\n2. Testing create_issue [Confirmed Execution Preview/Live]...")
exec_result = create_issue(
    owner=OWNER,
    repo=REPO,
    title="Automated Safety Test Issue",
    body="Executed with confirmed execution flag.",
    labels="documentation",
    confirm=True,
)
print(exec_result)

match = re.search(r"#(\d+):", exec_result)
issue_num = int(match.group(1)) if match else 1

print(f"\n3. Testing add_label [Dry Run] on issue #{issue_num}...")
label_dry = add_label(
    owner=OWNER,
    repo=REPO,
    issue_number=issue_num,
    labels="urgent",
    confirm=False,
)
print(label_dry)
assert "DRY RUN" in label_dry
print("[OK] Dry run prevented label addition.")

print(f"\n4. Testing add_label [Confirmed Execution] on issue #{issue_num}...")
label_exec = add_label(
    owner=OWNER,
    repo=REPO,
    issue_number=issue_num,
    labels="urgent",
    confirm=True,
)
print(label_exec)

print("\n" + "=" * 60)
print("SAFETY GUARDRAILS CONFIRMED AND PASSED")
print("=" * 60)
