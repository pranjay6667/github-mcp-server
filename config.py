"""
config.py — Loads configuration from environment variables.

WHY THIS FILE EXISTS:
- Your GitHub token is like a password. If it gets into your Git repo,
  anyone can use it to access your GitHub account.
- We store the token in a .env file (which is in .gitignore, so Git ignores it).
- This file reads .env and makes the token available to the rest of the code.
- If the token is missing, the program stops immediately with a clear error
  instead of crashing later with a confusing HTTP 401 error.
"""

import os
import sys

from dotenv import load_dotenv

# load_dotenv() reads the .env file in the project folder and puts its
# key=value pairs into os.environ, just as if you had set them in your
# terminal. This only affects the current Python process — it does not
# change your system environment variables.
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Fail early with a helpful message if the token is missing or still the
# placeholder from .env.example
if not GITHUB_TOKEN or GITHUB_TOKEN.startswith("ghp_paste"):
    print("=" * 60)
    print("ERROR: GITHUB_TOKEN is not set or is still the placeholder.")
    print()
    print("Fix it in 3 steps:")
    print("1. Copy .env.example to .env")
    print("2. Create a token at:")
    print("   https://github.com/settings/personal-access-tokens/new")
    print("3. Paste the token into .env")
    print("=" * 60)
    sys.exit(1)

# Base URL for the GitHub REST API — all our API calls start with this.
GITHUB_API_BASE = "https://api.github.com"
