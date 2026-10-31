"""Create test issues and labels on pranjay6667/Pranjay for testing our tools."""
import os
import time
os.chdir(r"C:\Users\pranj\.gemini\antigravity\scratch\github-mcp-server")

import httpx
from config import GITHUB_TOKEN

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}

OWNER = "pranjay6667"
REPO = "Pranjay"
BASE = "https://api.github.com"

def create_label(name, color, description):
    """Create a label on the repo."""
    r = httpx.post(
        f"{BASE}/repos/{OWNER}/{REPO}/labels",
        headers=headers,
        json={"name": name, "color": color, "description": description},
    )
    if r.status_code in (201, 422):  # 422 = already exists
        print(f"  Label '{name}': {'created' if r.status_code == 201 else 'already exists'}")
    else:
        print(f"  Label '{name}': error {r.status_code} - {r.text[:100]}")

def create_issue(title, body, labels=None):
    """Create an issue on the repo."""
    data = {"title": title, "body": body}
    if labels:
        data["labels"] = labels
    r = httpx.post(
        f"{BASE}/repos/{OWNER}/{REPO}/issues",
        headers=headers,
        json=data,
    )
    if r.status_code == 201:
        num = r.json()["number"]
        print(f"  Issue #{num}: '{title}' created")
        return num
    else:
        print(f"  Issue '{title}': error {r.status_code} - {r.text[:100]}")
        return None

# --- Create labels ---
print("Creating labels...")
create_label("bug", "d73a4a", "Something isn't working")
create_label("enhancement", "a2eeef", "New feature or request")
create_label("documentation", "0075ca", "Improvements or additions to docs")
create_label("urgent", "e11d48", "Needs immediate attention")

# --- Create issues ---
print("\nCreating issues...")
create_issue(
    "Login page crashes on mobile devices",
    "When opening the login page on Android Chrome, the page shows a white screen.\n\nSteps:\n1. Open the app on mobile\n2. Navigate to /login\n3. See blank page",
    labels=["bug"],
)
create_issue(
    "Add dark mode support",
    "Users have requested a dark mode option. This should respect the system preference and also have a manual toggle.",
    labels=["enhancement"],
)
create_issue(
    "Write API documentation for /users endpoint",
    "The /users endpoint is missing from our API docs. Need to add request/response examples.",
    labels=["documentation"],
)
create_issue(
    "Database connection timeout in production",
    "Getting intermittent connection timeouts to PostgreSQL in prod. Happens about 3 times per day.",
    labels=["bug", "urgent"],
)
create_issue(
    "Add unit tests for user authentication module",
    "The auth module has zero test coverage. Need at least 80% coverage.",
    labels=["enhancement"],
)

print("\nDone! Test data created.")
