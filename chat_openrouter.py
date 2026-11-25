"""
chat_openrouter.py — Interactive AI Chatbot powered by OpenRouter + GitHub MCP Server
Connects state-of-the-art LLMs (Claude 3.5, DeepSeek, Llama 3) to your 7 GitHub tools.
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment
PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    print("Error: OPENROUTER_API_KEY not found in .env file.")
    sys.exit(1)

# Import our 7 MCP tools directly from server.py
import server

# Map tool names to actual Python functions
TOOL_MAPPING = {
    "list_repos": server.list_repos,
    "list_open_issues": server.list_open_issues,
    "count_open_issues_all": server.count_open_issues_all,
    "get_repo_summary": server.get_repo_summary,
    "stale_issues": server.stale_issues,
    "create_issue": server.create_issue,
    "add_label": server.add_label,
}

# Convert MCP tools to OpenAI/OpenRouter Function Calling schemas
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "list_repos",
            "description": "List repositories belonging to the authenticated GitHub user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "visibility": {"type": "string", "enum": ["all", "public", "private"], "default": "all"},
                    "sort_by": {"type": "string", "enum": ["updated", "created", "pushed"], "default": "updated"},
                    "limit": {"type": "integer", "description": "Max repositories (1-100)", "default": 30}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_open_issues",
            "description": "List open issues for a specific repository. Filters out pull requests.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string", "description": "Repository owner (e.g. pranjay6667)"},
                    "repo": {"type": "string", "description": "Repository name (e.g. Pranjay)"},
                    "label": {"type": "string", "description": "Optional label filter (e.g. bug)", "default": ""},
                    "limit": {"type": "integer", "default": 30}
                },
                "required": ["owner", "repo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_open_issues_all",
            "description": "Count total open issues across ALL repositories owned by the user. Use when user asks for a global count across all repos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "label": {"type": "string", "description": "Optional label filter (e.g. bug)", "default": ""}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_repo_summary",
            "description": "Get a dashboard summary of a repository (metrics, recent commits, open PRs).",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string", "description": "Repository owner"},
                    "repo": {"type": "string", "description": "Repository name"}
                },
                "required": ["owner", "repo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "stale_issues",
            "description": "Find open issues in a repository with no activity for N days.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string", "description": "Repository owner"},
                    "repo": {"type": "string", "description": "Repository name"},
                    "days": {"type": "integer", "description": "Inactivity threshold in days", "default": 30}
                },
                "required": ["owner", "repo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_issue",
            "description": "Create a new issue in a GitHub repository. SAFETY: Defaults to DRY-RUN mode (confirm=False). Set confirm=True only after explicit user approval.",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "title": {"type": "string"},
                    "body": {"type": "string", "default": ""},
                    "labels": {"type": "string", "description": "Comma-separated labels", "default": ""},
                    "confirm": {"type": "boolean", "description": "Must be True to execute. False produces a dry-run preview.", "default": False}
                },
                "required": ["owner", "repo", "title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "add_label",
            "description": "Add one or more labels to an existing issue. SAFETY: Defaults to DRY-RUN mode (confirm=False).",
            "parameters": {
                "type": "object",
                "properties": {
                    "owner": {"type": "string"},
                    "repo": {"type": "string"},
                    "issue_number": {"type": "integer"},
                    "labels": {"type": "string", "description": "Comma-separated labels"},
                    "confirm": {"type": "boolean", "default": False}
                },
                "required": ["owner", "repo", "issue_number", "labels"]
            }
        }
    }
]

SYSTEM_PROMPT = (
    "You are an intelligent GitHub assistant powered by OpenRouter and connected to a local GitHub MCP Server. "
    "You have access to 7 tools to inspect repositories, issues, summaries, and create issues safely. "
    "SAFETY RULE: When creating an issue or adding labels, always first perform a dry run (confirm=False), "
    "show the preview to the user, and ask for explicit confirmation before executing with confirm=True. "
    "You understand queries in English, Hindi, and Hinglish. Answer clearly and concisely."
)

# Initialize OpenAI client for OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

MODELS = {
    "1": ("openrouter/auto", "Auto / Free Router (Universal & Robust - Recommended)"),
    "2": ("openai/gpt-4o-mini", "OpenAI GPT-4o Mini (Fast & Highly Accurate Tool Calling)"),
    "3": ("deepseek/deepseek-chat", "DeepSeek-V3 (Fast & Advanced Open Weights)"),
    "4": ("google/gemini-2.5-flash", "Google Gemini 2.5 Flash (Ultra-Fast Response)"),
}

def execute_tool_call(tool_name: str, args: dict) -> str:
    func = TOOL_MAPPING.get(tool_name)
    if not func:
        return f"Error: Tool '{tool_name}' not found."
    try:
        return func(**args)
    except Exception as e:
        return f"Tool Execution Error: {e}"

def main():
    print("=" * 65)
    print("  OPENROUTER AI ASSISTANT + GITHUB MCP SERVER")
    print("  MCA Minor Project Demo | Candidate: Pranjay")
    print("=" * 65)
    
    print("\nSelect an AI Model from OpenRouter:")
    for k, (m_id, desc) in MODELS.items():
        print(f"  [{k}] {desc}")
    
    choice = input("\nEnter choice [1-4, default=1]: ").strip() or "1"
    selected_model = MODELS.get(choice, MODELS["1"])[0]
    print(f"\n[Active Model]: {selected_model}")
    print("Type your questions in English, Hindi, or Hinglish (e.g. 'Show my repos', 'Mere open issues dikhao').")
    print("Type 'exit' or 'quit' to stop.\n" + "-" * 65)
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit", "q"):
                print("Exiting AI chat. Good luck with your viva!")
                break
                
            messages.append({"role": "user", "content": user_input})
            print("\n[AI thinking & selecting tools...]")
            
            # Call OpenRouter with tools
            response = client.chat.completions.create(
                model=selected_model,
                messages=messages,
                tools=TOOLS_SCHEMA,
                tool_choice="auto",
            )
            
            choice_msg = response.choices[0].message
            messages.append(choice_msg)
            
            # Check if model wants to call tools
            if choice_msg.tool_calls:
                for tc in choice_msg.tool_calls:
                    fn_name = tc.function.name
                    fn_args = json.loads(tc.function.arguments or "{}")
                    print(f"-> [MCP Tool Call]: {fn_name}({fn_args})")
                    
                    tool_output = execute_tool_call(fn_name, fn_args)
                    print(f"<- [Server Output]:\n{tool_output}\n")
                    
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "name": fn_name,
                        "content": str(tool_output)
                    })
                
                # Get final conversational response after tool execution
                second_response = client.chat.completions.create(
                    model=selected_model,
                    messages=messages,
                )
                final_text = second_response.choices[0].message.content
                print(f"Assistant: {final_text}")
                messages.append({"role": "assistant", "content": final_text})
            else:
                print(f"Assistant: {choice_msg.content}")
                
        except KeyboardInterrupt:
            print("\nExiting.")
            break
        except Exception as e:
            print(f"\n[Error]: {e}")

if __name__ == "__main__":
    main()
