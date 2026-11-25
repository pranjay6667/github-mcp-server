"""
demo.py — 1-Click Interactive Viva Demonstration Runner
Run this during your viva presentation to demonstrate all aspects of your project.
"""

import sys
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
PYTHON = sys.executable

def banner():
    print("=" * 65)
    print("  GITHUB MCP SERVER — FINAL VIVA DEMONSTRATION")
    print("  MCA Minor Project | VIPS-TC, GGSIPU, Delhi")
    print("  Candidate: Pranjay (github.com/pranjay6667/github-mcp-server)")
    print("=" * 65)

def menu():
    print("\nSelect a Demonstration Action:")
    print("  [1] Live Tool Suite Test (All 7 Tools against GitHub API)")
    print("  [2] Safety Guardrail Verification (Dry-Run vs Confirmed Write)")
    print("  [3] MCP Protocol & Schema Verification (In-Process)")
    print("  [4] 50-Question Multilingual Benchmark (98% Accuracy)")
    print("  [5] Launch MCP Inspector Web UI (Interactive Browser Dashboard)")
    print("  [0] Exit")
    print("-" * 65)

def run_script(rel_path):
    script = PROJECT_ROOT / rel_path
    print(f"\n>>> Executing: python {rel_path} ...\n")
    subprocess.run([PYTHON, str(script)], check=False)

def launch_inspector():
    print("\n>>> Launching MCP Inspector (http://localhost:6274) ...")
    print("Press Ctrl+C in terminal when finished.\n")
    subprocess.run(["mcp", "dev", "server.py"], shell=True)

def main():
    banner()
    while True:
        menu()
        choice = input("Enter option [1-5, or 0]: ").strip()
        if choice == "1":
            run_script("tests/test_tools.py")
        elif choice == "2":
            run_script("tests/test_safety.py")
        elif choice == "3":
            run_script("tests/test_protocol.py")
        elif choice == "4":
            run_script("evaluation/evaluate.py")
        elif choice == "5":
            launch_inspector()
        elif choice in ("0", "exit", "q"):
            print("\nExiting demo. Best of luck for your viva!\n")
            break
        else:
            print("Invalid selection. Please choose 1, 2, 3, 4, 5, or 0.")

if __name__ == "__main__":
    main()
