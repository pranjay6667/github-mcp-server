"""GitHub REST API client with authentication, pagination, and rate limit handling."""

import logging
import sys
import time
from datetime import datetime, timezone
from typing import Any, Optional
import httpx

from config import GITHUB_TOKEN, GITHUB_API_BASE

# Log only to stderr to preserve stdout for MCP JSON-RPC protocol
logger = logging.getLogger("github_mcp")
if not logger.handlers:
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(
        logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class GitHubClient:
    """Wrapper around GitHub REST API with auth, pagination, and error handling."""

    def __init__(self) -> None:
        self.client = httpx.Client(
            base_url=GITHUB_API_BASE,
            headers={
                "Authorization": f"Bearer {GITHUB_TOKEN}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=30.0,
        )
        self._username: Optional[str] = None

    @property
    def username(self) -> str:
        """Return the authenticated user's GitHub username (cached)."""
        if self._username is None:
            user = self.get_authenticated_user()
            self._username = user["login"]
        return self._username

    # ------------------------------------------------------------------
    # Rate Limiting & Response Handling
    # ------------------------------------------------------------------

    def _check_rate_limit(self, response: httpx.Response) -> None:
        """Inspect rate limit headers and warn or raise when near quota."""
        remaining = response.headers.get("x-ratelimit-remaining")
        limit = response.headers.get("x-ratelimit-limit")

        if remaining is not None:
            rem_int = int(remaining)
            if rem_int < 10:
                logger.warning("Low GitHub API rate limit: %d/%s remaining", rem_int, limit)
            if rem_int == 0:
                reset_ts = int(response.headers.get("x-ratelimit-reset", 0))
                reset_time = datetime.fromtimestamp(reset_ts, tz=timezone.utc)
                wait_sec = max(reset_ts - int(time.time()), 1)
                raise RuntimeError(
                    f"GitHub API rate limit exhausted. Resets at "
                    f"{reset_time.strftime('%H:%M:%S UTC')} ({wait_sec}s)."
                )

    def _handle_response(self, response: httpx.Response) -> Any:
        """Validate HTTP response and return parsed JSON payload."""
        self._check_rate_limit(response)

        if response.status_code == 401:
            raise RuntimeError("Authentication failed (HTTP 401). Token is invalid or expired.")
        if response.status_code == 403:
            raise RuntimeError("Access forbidden (HTTP 403). Check token permissions or rate limit.")
        if response.status_code == 404:
            raise RuntimeError("Resource not found (HTTP 404). Verify owner, repository, or issue number.")
        if response.status_code == 409:
            return []  # Empty repository (e.g. no commits)
        if response.status_code == 422:
            detail = response.json().get("message", response.text[:200])
            raise RuntimeError(f"Validation error (HTTP 422): {detail}")
        if response.status_code >= 400:
            raise RuntimeError(f"GitHub API error (HTTP {response.status_code}): {response.text[:200]}")

        return response.json()

    # ------------------------------------------------------------------
    # Pagination
    # ------------------------------------------------------------------

    def _get_paginated(
        self, path: str, params: Optional[dict[str, Any]] = None, limit: int = 30
    ) -> list[dict[str, Any]]:
        """Fetch items sequentially following 'Link: rel=next' pagination headers."""
        if params is None:
            params = {}
        params["per_page"] = min(limit, 100)

        all_results: list[dict[str, Any]] = []
        url: Optional[str] = path
        is_first = True

        while url and len(all_results) < limit:
            logger.info("Fetching: %s", url)
            if is_first:
                resp = self.client.get(url, params=params)
                is_first = False
            else:
                resp = self.client.get(url)

            data = self._handle_response(resp)
            if isinstance(data, list):
                all_results.extend(data)
            else:
                return data

            url = self._get_next_page_url(resp)

        return all_results[:limit]

    @staticmethod
    def _get_next_page_url(response: httpx.Response) -> Optional[str]:
        link_header = response.headers.get("link", "")
        for part in link_header.split(","):
            if 'rel="next"' in part:
                return part.split(";")[0].strip().strip("<>")
        return None

    # ------------------------------------------------------------------
    # GitHub REST Endpoints
    # ------------------------------------------------------------------

    def get_authenticated_user(self) -> dict[str, Any]:
        """Fetch authenticated user profile."""
        resp = self.client.get("/user")
        return self._handle_response(resp)

    def list_repos(
        self, visibility: str = "all", sort: str = "updated", limit: int = 30
    ) -> list[dict[str, Any]]:
        """List repositories for the authenticated user."""
        params = {"visibility": visibility, "sort": sort, "direction": "desc"}
        return self._get_paginated("/user/repos", params=params, limit=limit)

    def list_open_issues(
        self, owner: str, repo: str, label: Optional[str] = None, limit: int = 30
    ) -> list[dict[str, Any]]:
        """List open issues for a repository, filtering out pull requests."""
        params: dict[str, Any] = {"state": "open", "sort": "created", "direction": "desc"}
        if label:
            params["labels"] = label

        items = self._get_paginated(f"/repos/{owner}/{repo}/issues", params=params, limit=limit + 20)
        issues_only = [item for item in items if "pull_request" not in item]
        return issues_only[:limit]

    def count_open_issues_all(self, label: Optional[str] = None) -> dict[str, Any]:
        """Count total open issues across all user repos using Search API."""
        query = f"is:issue is:open author:{self.username}"
        if label:
            query += f" label:{label}"
        logger.info("Search query: %s", query)
        resp = self.client.get("/search/issues", params={"q": query, "per_page": 100})
        return self._handle_response(resp)

    def get_repo_details(self, owner: str, repo: str) -> dict[str, Any]:
        """Get repository metadata."""
        resp = self.client.get(f"/repos/{owner}/{repo}")
        return self._handle_response(resp)

    def get_recent_commits(self, owner: str, repo: str, limit: int = 5) -> list[dict[str, Any]]:
        """Fetch recent commits on default branch."""
        resp = self.client.get(f"/repos/{owner}/{repo}/commits", params={"per_page": limit})
        return self._handle_response(resp)

    def get_open_pull_requests(self, owner: str, repo: str, limit: int = 5) -> list[dict[str, Any]]:
        """Fetch open pull requests."""
        resp = self.client.get(f"/repos/{owner}/{repo}/pulls", params={"state": "open", "per_page": limit})
        return self._handle_response(resp)

    def get_stale_issues(self, owner: str, repo: str, days: int = 30) -> list[dict[str, Any]]:
        """Find open issues with no updates for N days (sorted ascending by update)."""
        params = {"state": "open", "sort": "updated", "direction": "asc", "per_page": 100}
        items = self._get_paginated(f"/repos/{owner}/{repo}/issues", params=params, limit=100)
        issues_only = [item for item in items if "pull_request" not in item]

        now = datetime.now(timezone.utc)
        stale = []
        for issue in issues_only:
            updated_str = issue.get("updated_at", "")
            if not updated_str:
                continue
            updated = datetime.fromisoformat(updated_str.replace("Z", "+00:00"))
            days_since = (now - updated).days
            if days_since >= days:
                issue["_days_stale"] = days_since
                stale.append(issue)
            else:
                break
        return stale

    def create_issue(
        self, owner: str, repo: str, title: str, body: str = "", labels: Optional[list[str]] = None
    ) -> dict[str, Any]:
        """Create a new issue."""
        data: dict[str, Any] = {"title": title, "body": body}
        if labels:
            data["labels"] = labels
        logger.info("Creating issue in %s/%s: '%s'", owner, repo, title)
        resp = self.client.post(f"/repos/{owner}/{repo}/issues", json=data)
        return self._handle_response(resp)

    def add_labels_to_issue(
        self, owner: str, repo: str, issue_number: int, labels: list[str]
    ) -> list[dict[str, Any]]:
        """Attach labels to an existing issue."""
        logger.info("Adding labels %s to %s/%s#%d", labels, owner, repo, issue_number)
        resp = self.client.post(f"/repos/{owner}/{repo}/issues/{issue_number}/labels", json={"labels": labels})
        return self._handle_response(resp)
