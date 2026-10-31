"""Test that the GitHub token works and can access the API."""
import os
import sys

# Load .env
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("GITHUB_TOKEN")
if not token:
    print("ERROR: GITHUB_TOKEN not found in .env")
    sys.exit(1)

print(f"Token loaded: {token[:15]}...{token[-4:]}  (middle hidden for safety)")

# Test the token by calling GitHub API
import httpx

response = httpx.get(
    "https://api.github.com/user",
    headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    },
)

if response.status_code == 200:
    user = response.json()
    print(f"\nTOKEN WORKS! (HTTP 200)")
    print(f"   GitHub username: {user['login']}")
    print(f"   Name: {user.get('name', 'not set')}")
    print(f"   Public repos: {user.get('public_repos', 0)}")
    print(f"   Rate limit remaining: {response.headers.get('x-ratelimit-remaining', '?')}/5000")
elif response.status_code == 401:
    print(f"\nTOKEN INVALID (HTTP 401). Create a new one at:")
    print("   https://github.com/settings/personal-access-tokens/new")
else:
    print(f"\nUnexpected error: HTTP {response.status_code}")
    print(f"   {response.text[:200]}")
