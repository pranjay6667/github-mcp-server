"""Configuration loader for GitHub MCP Server."""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Resolve .env relative to this file to support execution from any cwd
_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_BASE = "https://api.github.com"

if not GITHUB_TOKEN or GITHUB_TOKEN.startswith("ghp_paste"):
    sys.stderr.write(
        "Error: GITHUB_TOKEN is not configured.\n"
        "Copy .env.example to .env and set your personal access token.\n"
    )
    sys.exit(1)
