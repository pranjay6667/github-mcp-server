"""Test the list_repos tool by calling it directly."""
import os
import sys

# Make sure we're in the project directory so .env is found
os.chdir(r"C:\Users\pranj\.gemini\antigravity\scratch\github-mcp-server")

# Import and call the tool function directly
from server import list_repos

print("=== Test 1: List all repos (default) ===")
result = list_repos()
print(result)

print("\n=== Test 2: List only public repos ===")
result = list_repos(visibility="public", limit=5)
print(result)

print("\n=== Test 3: Invalid visibility (should show error) ===")
result = list_repos(visibility="xyz")
print(result)

print("\nALL TESTS DONE")
