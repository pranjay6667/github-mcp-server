"""Seed test issues and labels in the target repository for local development."""

import sys
from pathlib import Path
import httpx

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import GITHUB_TOKEN
from github_client import GitHubClient

client = GitHubClient()
OWNER = client.username
REPO = "Pranjay"
BASE = "https://api.github.com"

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}


def create_label(name: str, color: str, description: str) -> None:
    r = httpx.post(
        f"{BASE}/repos/{OWNER}/{REPO}/labels",
        headers=headers,
        json={"name": name, "color": color, "description": description},
    )
    if r.status_code in (201, 422):
        status = "created" if r.status_code == 201 else "already exists"
        print(f"  Label '{name}': {status}")
    else:
        print(f"  Label '{name}': error {r.status_code} - {r.text[:100]}")


def create_issue(title: str, body: str, labels: list[str] | None = None) -> int | None:
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
    print(f"  Issue '{title}': error {r.status_code} - {r.text[:100]}")
    return None


def main() -> None:
    print(f"Seeding test data for repository {OWNER}/{REPO}...\n")

    print("Labels:")
    create_label("bug", "d73a4a", "Something is not working")
    create_label("enhancement", "a2eeef", "New feature request")
    create_label("documentation", "0075ca", "Improvements or additions to docs")
    create_label("urgent", "e11d48", "Needs immediate attention")

    print("\nIssues:")
    create_issue(
        "Login page crashes on mobile devices",
        "When opening the login page on Android Chrome, the page shows a blank screen.",
        labels=["bug"],
    )
    create_issue(
        "Add dark mode support",
        "Users have requested a dark mode option with system auto-detection and manual toggle.",
        labels=["enhancement"],
    )
    create_issue(
        "Write API documentation for /users endpoint",
        "Add request/response examples and schema docs.",
        labels=["documentation"],
    )
    create_issue(
        "Database connection timeout in production",
        "Intermittent connection timeouts to PostgreSQL in prod environment.",
        labels=["bug", "urgent"],
    )

    print("\nData seeding completed.")


if __name__ == "__main__":
    main()
