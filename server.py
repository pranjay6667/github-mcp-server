"""
server.py — GitHub MCP Server

Main entry point registering all 7 tools for the AI assistant.
Logging routes to stderr to ensure stdio JSON-RPC protocol messages are untouched.
"""

import logging
import sys
from mcp.server.mcpserver import MCPServer
from github_client import GitHubClient

logger = logging.getLogger("github_mcp")

# Initialize MCP Server
mcp = MCPServer(
    name="github-mcp-server",
    instructions=(
        "A server connecting AI assistants to authenticated GitHub data. "
        "Exposes read-only tools for browsing repositories, issues, summaries, "
        "and stale backlogs. Write tools (create_issue, add_label) require explicit "
        "user confirmation (confirm=True) after showing a dry-run preview."
    ),
)

# API client
client = GitHubClient()


# ================================================================== #
#                         READ-ONLY TOOLS                            #
# ================================================================== #

@mcp.tool()
def list_repos(
    visibility: str = "all",
    sort_by: str = "updated",
    limit: int = 30,
) -> str:
    """
    List repositories belonging to the authenticated GitHub user.

    Args:
        visibility: "all", "public", or "private". Defaults to "all".
        sort_by: "updated", "created", or "pushed". Defaults to "updated".
        limit: Max repos to return (1-100). Defaults to 30.
    """
    valid_visibility = ("all", "public", "private")
    if visibility not in valid_visibility:
        return f"Error: visibility must be one of {valid_visibility}, got '{visibility}'."

    valid_sort = ("updated", "created", "pushed")
    if sort_by not in valid_sort:
        return f"Error: sort_by must be one of {valid_sort}, got '{sort_by}'."

    limit = max(1, min(limit, 100))

    try:
        repos = client.list_repos(visibility=visibility, sort=sort_by, limit=limit)
    except Exception as e:
        logger.error("list_repos failed: %s", e)
        return f"Error: {e}"

    if not repos:
        return "You have no repositories matching this filter."

    lines = [f"Found {len(repos)} repositories:\n"]
    for i, repo in enumerate(repos, 1):
        desc = repo.get("description") or "No description"
        if len(desc) > 80:
            desc = desc[:77] + "..."
        language = repo.get("language") or "Not set"
        private_label = "Private" if repo.get("private") else "Public"
        stars = repo.get("stargazers_count", 0)
        forks = repo.get("forks_count", 0)
        issues = repo.get("open_issues_count", 0)
        updated = repo.get("updated_at", "Unknown")[:10]
        url = repo.get("html_url", "")

        lines.append(
            f"{i}. {repo['full_name']} [{private_label}]\n"
            f"   {desc}\n"
            f"   Language: {language} | Stars: {stars} | Forks: {forks} | Open issues: {issues}\n"
            f"   Last updated: {updated} | {url}\n"
        )

    return "\n".join(lines)


@mcp.tool()
def list_open_issues(
    owner: str,
    repo: str,
    label: str = "",
    limit: int = 30,
) -> str:
    """
    List open issues for a specific repository.

    Args:
        owner: The repository owner (GitHub username), e.g. "pranjay6667".
        repo: The repository name, e.g. "Pranjay".
        label: Optional label filter (e.g. "bug").
        limit: Max issues to return (1-100). Defaults to 30.
    """
    if not owner or not repo:
        return "Error: both 'owner' and 'repo' are required."

    limit = max(1, min(limit, 100))
    label_filter = label if label else None

    try:
        issues = client.list_open_issues(owner=owner, repo=repo, label=label_filter, limit=limit)
    except Exception as e:
        logger.error("list_open_issues failed: %s", e)
        return f"Error: {e}"

    if not issues:
        msg = f"No open issues found in {owner}/{repo}"
        if label:
            msg += f" with label '{label}'"
        return msg + "."

    lines = [f"Open issues in {owner}/{repo}" + (f" (label: {label})" if label else "") + f" — {len(issues)} found:\n"]
    for issue in issues:
        number = issue.get("number", "?")
        title = issue.get("title", "Untitled")
        labels = [l["name"] for l in issue.get("labels", [])]
        author = issue.get("user", {}).get("login", "unknown")
        created = issue.get("created_at", "")[:10]
        updated = issue.get("updated_at", "")[:10]
        url = issue.get("html_url", "")
        label_str = ", ".join(labels) if labels else "none"

        lines.append(
            f"  #{number}: {title}\n"
            f"    Labels: [{label_str}] | Author: {author}\n"
            f"    Created: {created} | Updated: {updated}\n"
            f"    {url}\n"
        )

    return "\n".join(lines)


@mcp.tool()
def count_open_issues_all(label: str = "") -> str:
    """
    Count total open issues across ALL repositories owned by the user.

    Args:
        label: Optional label filter, e.g. "bug".
    """
    label_filter = label if label else None

    try:
        result = client.count_open_issues_all(label=label_filter)
    except Exception as e:
        logger.error("count_open_issues_all failed: %s", e)
        return f"Error: {e}"

    total = result.get("total_count", 0)
    items = result.get("items", [])

    if total == 0:
        msg = "You have no open issues across any repository"
        if label:
            msg += f" with label '{label}'"
        return msg + "."

    repo_counts = {}
    for item in items:
        repo_full = item.get("repository_url", "").replace("https://api.github.com/repos/", "")
        repo_counts[repo_full] = repo_counts.get(repo_full, 0) + 1

    lines = [f"Total open issues: {total}" + (f" (label: {label})" if label else "") + "\n"]
    lines.append("Per-repository breakdown:")
    for repo_full, count in sorted(repo_counts.items(), key=lambda x: x[1], reverse=True):
        lines.append(f"  {repo_full}: {count} open issues")

    return "\n".join(lines)


@mcp.tool()
def get_repo_summary(owner: str, repo: str) -> str:
    """
    Get a dashboard-style summary of a repository (metrics, recent commits, open PRs).

    Args:
        owner: The repository owner (GitHub username).
        repo: The repository name.
    """
    if not owner or not repo:
        return "Error: both 'owner' and 'repo' are required."

    try:
        details = client.get_repo_details(owner, repo)
        commits = client.get_recent_commits(owner, repo, limit=5)
        prs = client.get_open_pull_requests(owner, repo, limit=5)
    except Exception as e:
        logger.error("get_repo_summary failed: %s", e)
        return f"Error: {e}"

    desc = details.get("description") or "No description"
    language = details.get("language") or "Not set"
    stars = details.get("stargazers_count", 0)
    forks = details.get("forks_count", 0)
    open_issues = details.get("open_issues_count", 0)
    created = details.get("created_at", "")[:10]
    updated = details.get("updated_at", "")[:10]
    url = details.get("html_url", "")
    private_label = "Private" if details.get("private") else "Public"

    lines = [
        f"Repository: {details.get('full_name', f'{owner}/{repo}')} [{private_label}]",
        f"Description: {desc}",
        f"Language: {language} | Stars: {stars} | Forks: {forks}",
        f"Open issues: {open_issues}",
        f"Created: {created} | Last updated: {updated}",
        f"URL: {url}",
    ]

    if isinstance(commits, list) and commits:
        lines.append(f"\nRecent commits ({len(commits)}):")
        for c in commits[:5]:
            msg = c.get("commit", {}).get("message", "").split("\n")[0]
            author = c.get("commit", {}).get("author", {}).get("name", "unknown")
            date = c.get("commit", {}).get("author", {}).get("date", "")[:10]
            lines.append(f"  - [{date}] {msg} (by {author})")
    else:
        lines.append("\nNo commits yet.")

    if isinstance(prs, list) and prs:
        lines.append(f"\nOpen pull requests ({len(prs)}):")
        for pr in prs[:5]:
            lines.append(
                f"  - #{pr.get('number', '?')}: {pr.get('title', 'Untitled')} "
                f"(by {pr.get('user', {}).get('login', 'unknown')})"
            )
    else:
        lines.append("\nNo open pull requests.")

    return "\n".join(lines)


@mcp.tool()
def stale_issues(
    owner: str,
    repo: str,
    days: int = 30,
) -> str:
    """
    Find open issues in a repository with no activity for N days.

    Args:
        owner: Repository owner.
        repo: Repository name.
        days: Inactivity threshold in days (default: 30).
    """
    if not owner or not repo:
        return "Error: both 'owner' and 'repo' are required."
    days = max(1, days)

    try:
        stale = client.get_stale_issues(owner=owner, repo=repo, days=days)
    except Exception as e:
        logger.error("stale_issues failed: %s", e)
        return f"Error: {e}"

    if not stale:
        return f"No stale issues found in {owner}/{repo}. All open issues have had activity in the last {days} days."

    lines = [f"Stale issues in {owner}/{repo} (no activity for {days}+ days) — {len(stale)} found:\n"]
    for issue in stale:
        number = issue.get("number", "?")
        title = issue.get("title", "Untitled")
        days_stale = issue.get("_days_stale", "?")
        updated = issue.get("updated_at", "")[:10]
        labels = [l["name"] for l in issue.get("labels", [])]
        label_str = ", ".join(labels) if labels else "none"
        url = issue.get("html_url", "")

        lines.append(
            f"  #{number}: {title}\n"
            f"    Last activity: {updated} ({days_stale} days ago)\n"
            f"    Labels: [{label_str}]\n"
            f"    {url}\n"
        )

    return "\n".join(lines)


# ================================================================== #
#              WRITE TOOLS (Require confirm=True)                    #
# ================================================================== #

@mcp.tool()
def create_issue(
    owner: str,
    repo: str,
    title: str,
    body: str = "",
    labels: str = "",
    confirm: bool = False,
) -> str:
    """
    Create a new issue in a GitHub repository.

    SAFETY: Defaults to DRY-RUN mode (confirm=False). Shows preview.
    Set confirm=True only after explicit user confirmation.

    Args:
        owner: Repository owner.
        repo: Repository name.
        title: Issue title (required).
        body: Optional description.
        labels: Comma-separated labels, e.g. "bug,urgent".
        confirm: Must be True to execute. False produces a preview.
    """
    if not owner or not repo:
        return "Error: both 'owner' and 'repo' are required."
    if not title or not title.strip():
        return "Error: 'title' is required and cannot be empty."

    label_list = [l.strip() for l in labels.split(",") if l.strip()] if labels else []

    # Dry-run preview
    if not confirm:
        return (
            "DRY RUN — Issue preview (not created yet):\n\n"
            f"  Repository: {owner}/{repo}\n"
            f"  Title: {title}\n"
            f"  Body: {body if body else '(empty)'}\n"
            f"  Labels: {label_list if label_list else '(none)'}\n\n"
            "To actually create this issue, call create_issue again with confirm=True."
        )

    # Execution
    try:
        result = client.create_issue(
            owner=owner, repo=repo, title=title, body=body, labels=label_list if label_list else None
        )
    except Exception as e:
        logger.error("create_issue failed: %s", e)
        return f"Error: {e}"

    number = result.get("number", "?")
    url = result.get("html_url", "")
    return f"Issue created successfully!\n  #{number}: {title}\n  URL: {url}"


@mcp.tool()
def add_label(
    owner: str,
    repo: str,
    issue_number: int,
    labels: str,
    confirm: bool = False,
) -> str:
    """
    Add one or more labels to an existing issue.

    SAFETY: Defaults to DRY-RUN mode (confirm=False). Shows preview.
    Set confirm=True only after explicit user confirmation.

    Args:
        owner: Repository owner.
        repo: Repository name.
        issue_number: Issue number (positive integer).
        labels: Comma-separated labels to add, e.g. "bug,urgent".
        confirm: Must be True to execute. False produces a preview.
    """
    if not owner or not repo:
        return "Error: both 'owner' and 'repo' are required."
    if issue_number < 1:
        return "Error: 'issue_number' must be a positive integer."

    label_list = [l.strip() for l in labels.split(",") if l.strip()]
    if not label_list:
        return "Error: 'labels' is required. Provide comma-separated label names."

    # Dry-run preview
    if not confirm:
        return (
            "DRY RUN — Label preview (not added yet):\n\n"
            f"  Repository: {owner}/{repo}\n"
            f"  Issue: #{issue_number}\n"
            f"  Labels to add: {label_list}\n\n"
            "To actually add these labels, call add_label again with confirm=True."
        )

    # Execution
    try:
        result = client.add_labels_to_issue(
            owner=owner, repo=repo, issue_number=issue_number, labels=label_list
        )
    except Exception as e:
        logger.error("add_label failed: %s", e)
        return f"Error: {e}"

    added = [l.get("name", "?") for l in result] if isinstance(result, list) else []
    return f"Labels added successfully to #{issue_number}!\n  Current labels: {added}"


if __name__ == "__main__":
    mcp.run()
