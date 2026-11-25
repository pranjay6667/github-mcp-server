"""
app_web.py — Modern Web Interface for GitHub MCP Server + OpenRouter AI
Serves an interactive web application at http://localhost:8000.
"""

import os
import sys
import json
import webbrowser
from pathlib import Path
from dotenv import load_dotenv

# Ensure server module is accessible
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

import uvicorn
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route
from openai import OpenAI

import server
from chat_openrouter import TOOLS_SCHEMA, TOOL_MAPPING, execute_tool_call, SYSTEM_PROMPT, MODELS

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

HTML_PAGE = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GitHub MCP Server & AI Assistant</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: { 500: '#6366f1', 600: '#4f46e5', 700: '#4338ca' }
          }
        }
      }
    }
  </script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .chat-bubble { max-width: 82%; word-wrap: break-word; }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col">

  <!-- Header -->
  <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center text-white shadow-lg shadow-indigo-500/30">
          <i class="fab fa-github text-xl"></i>
        </div>
        <div>
          <h1 class="text-base font-bold text-white leading-tight">GitHub MCP Server</h1>
          <p class="text-xs text-slate-400">Model Context Protocol • MCA Minor Project (Pranjay)</p>
        </div>
      </div>

      <div class="flex items-center space-x-3">
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-950 text-emerald-400 border border-emerald-800">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-1.5 animate-pulse"></span>
          MCP Server Active (7 Tools)
        </span>
        <select id="modelSelect" class="bg-slate-800 text-xs border border-slate-700 rounded-lg px-3 py-1.5 text-slate-200 focus:outline-none focus:border-indigo-500">
          <option value="openrouter/auto">Auto / Free Router (Universal)</option>
          <option value="openai/gpt-4o-mini">OpenAI GPT-4o Mini</option>
          <option value="deepseek/deepseek-chat">DeepSeek-V3</option>
          <option value="google/gemini-2.5-flash">Google Gemini 2.5 Flash</option>
        </select>
      </div>
    </div>
  </header>

  <!-- Main Content Grid -->
  <main class="max-w-7xl mx-auto px-4 py-6 flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6 w-full">
    
    <!-- Left Column: Tool Suite & Fast Actions (5 Cols) -->
    <div class="lg:col-span-5 space-y-5 flex flex-col">
      <!-- Quick Info Card -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm">
        <h2 class="text-sm font-semibold text-white uppercase tracking-wider mb-3 flex items-center">
          <i class="fas fa-microchip text-indigo-400 mr-2"></i> MCP Protocol Architecture
        </h2>
        <p class="text-xs text-slate-400 leading-relaxed">
          Standardized JSON-RPC 2.0 communication exposing GitHub REST APIs as validated agentic tools with dry-run mutation guardrails.
        </p>
        <div class="grid grid-cols-2 gap-3 mt-4 text-xs">
          <div class="bg-slate-800/60 p-2.5 rounded-xl border border-slate-700/50">
            <span class="text-slate-400 block text-[10px] uppercase">Candidate</span>
            <span class="font-semibold text-slate-200">Pranjay (00417704424)</span>
          </div>
          <div class="bg-slate-800/60 p-2.5 rounded-xl border border-slate-700/50">
            <span class="text-slate-400 block text-[10px] uppercase">Benchmark</span>
            <span class="font-semibold text-emerald-400">98% Accuracy (49/50)</span>
          </div>
        </div>
      </div>

      <!-- Quick Action Buttons -->
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-sm flex-1 flex flex-col">
        <h2 class="text-sm font-semibold text-white uppercase tracking-wider mb-3 flex items-center">
          <i class="fas fa-bolt text-amber-400 mr-2"></i> 1-Click Fast Actions
        </h2>
        <p class="text-xs text-slate-400 mb-3">Execute any of the 7 MCP tools directly against authenticated GitHub API:</p>
        
        <div class="space-y-2 flex-1 overflow-y-auto pr-1 text-xs">
          <button onclick="runQuickPrompt('Show all my GitHub repositories')" class="w-full text-left p-3 rounded-xl bg-slate-800 hover:bg-slate-700/80 border border-slate-700/60 transition flex items-center justify-between group">
            <div>
              <div class="font-medium text-slate-200 group-hover:text-indigo-300">📁 List My Repositories</div>
              <div class="text-[11px] text-slate-400">Tool: list_repos</div>
            </div>
            <i class="fas fa-arrow-right text-slate-500 group-hover:text-indigo-400 text-xs transition"></i>
          </button>

          <button onclick="runQuickPrompt('List open issues in repository pranjay6667/Pranjay')" class="w-full text-left p-3 rounded-xl bg-slate-800 hover:bg-slate-700/80 border border-slate-700/60 transition flex items-center justify-between group">
            <div>
              <div class="font-medium text-slate-200 group-hover:text-indigo-300">🐛 List Open Issues</div>
              <div class="text-[11px] text-slate-400">Repo: pranjay6667/Pranjay</div>
            </div>
            <i class="fas fa-arrow-right text-slate-500 group-hover:text-indigo-400 text-xs transition"></i>
          </button>

          <button onclick="runQuickPrompt('Get summary and metrics for repository pranjay6667/Pranjay')" class="w-full text-left p-3 rounded-xl bg-slate-800 hover:bg-slate-700/80 border border-slate-700/60 transition flex items-center justify-between group">
            <div>
              <div class="font-medium text-slate-200 group-hover:text-indigo-300">📊 Repo Metrics & Summary</div>
              <div class="text-[11px] text-slate-400">Tool: get_repo_summary</div>
            </div>
            <i class="fas fa-arrow-right text-slate-500 group-hover:text-indigo-400 text-xs transition"></i>
          </button>

          <button onclick="runQuickPrompt('Find stale issues with no activity for more than 10 days in pranjay6667/Pranjay')" class="w-full text-left p-3 rounded-xl bg-slate-800 hover:bg-slate-700/80 border border-slate-700/60 transition flex items-center justify-between group">
            <div>
              <div class="font-medium text-slate-200 group-hover:text-indigo-300">⏳ Check Stale Issues</div>
              <div class="text-[11px] text-slate-400">Tool: stale_issues (10+ days)</div>
            </div>
            <i class="fas fa-arrow-right text-slate-500 group-hover:text-indigo-400 text-xs transition"></i>
          </button>

          <button onclick="runQuickPrompt('Create an issue titled Sample Bug in pranjay6667/Pranjay')" class="w-full text-left p-3 rounded-xl bg-amber-950/30 hover:bg-amber-900/40 border border-amber-800/40 transition flex items-center justify-between group">
            <div>
              <div class="font-medium text-amber-200 group-hover:text-amber-100">🛡️ Test Safety Guardrail (Dry-Run)</div>
              <div class="text-[11px] text-amber-400/80">confirm=False (Preview Only)</div>
            </div>
            <i class="fas fa-shield-alt text-amber-400 text-xs"></i>
          </button>
        </div>
      </div>
    </div>

    <!-- Right Column: Live AI Chat Interface (7 Cols) -->
    <div class="lg:col-span-7 bg-slate-900 border border-slate-800 rounded-2xl flex flex-col shadow-sm overflow-hidden h-[680px]">
      
      <!-- Chat Header -->
      <div class="p-4 border-b border-slate-800 bg-slate-900/60 flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <div class="w-2.5 h-2.5 rounded-full bg-indigo-500"></div>
          <span class="text-xs font-semibold text-slate-200">Interactive OpenRouter AI Conversation</span>
        </div>
        <button onclick="clearChat()" class="text-xs text-slate-400 hover:text-slate-200 flex items-center space-x-1">
          <i class="fas fa-trash-alt text-[10px]"></i>
          <span>Clear</span>
        </button>
      </div>

      <!-- Chat Messages Container -->
      <div id="chatMessages" class="flex-1 p-4 overflow-y-auto space-y-4 text-xs">
        <!-- Assistant Welcome -->
        <div class="flex items-start space-x-3">
          <div class="w-7 h-7 rounded-lg bg-indigo-600 flex items-center justify-center text-white shrink-0 mt-0.5">
            <i class="fas fa-robot text-xs"></i>
          </div>
          <div class="chat-bubble bg-slate-800 border border-slate-700/70 p-3.5 rounded-2xl rounded-tl-sm text-slate-200">
            <p class="font-medium text-indigo-300 mb-1">Hello Pranjay!</p>
            <p>I am your MCP-enabled AI Assistant. Ask me anything in English, Hindi, or Hinglish about your GitHub repositories, issues, commits, or safety rules.</p>
          </div>
        </div>
      </div>

      <!-- Tool Execution Indicator -->
      <div id="toolIndicator" class="hidden px-4 py-2 bg-indigo-950/40 border-t border-indigo-900/40 text-[11px] text-indigo-300 flex items-center space-x-2">
        <i class="fas fa-cog fa-spin text-indigo-400"></i>
        <span id="toolIndicatorText">Calling MCP Tool...</span>
      </div>

      <!-- Chat Input Form -->
      <form id="chatForm" onsubmit="sendMessage(event)" class="p-3 border-t border-slate-800 bg-slate-900 flex items-center space-x-2">
        <input 
          id="userInput" 
          type="text" 
          placeholder="Ask a question (e.g. 'Show my repos', 'Mere open issues dikhao')..." 
          class="flex-1 bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-xs text-slate-100 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
          autocomplete="off"
        />
        <button 
          id="sendBtn"
          type="submit" 
          class="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2.5 rounded-xl text-xs font-medium transition flex items-center space-x-1.5 shadow-md shadow-indigo-600/20"
        >
          <span>Send</span>
          <i class="fas fa-paper-plane text-[10px]"></i>
        </button>
      </form>
    </div>

  </main>

  <script>
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    const toolIndicator = document.getElementById('toolIndicator');
    const toolIndicatorText = document.getElementById('toolIndicatorText');
    const modelSelect = document.getElementById('modelSelect');

    let history = [];

    function appendMessage(role, text, toolCall = null) {
      const isUser = role === 'user';
      const wrapper = document.createElement('div');
      wrapper.className = `flex items-start space-x-3 ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`;

      const avatar = document.createElement('div');
      avatar.className = `w-7 h-7 rounded-lg flex items-center justify-center text-white shrink-0 mt-0.5 ${isUser ? 'bg-emerald-600' : 'bg-indigo-600'}`;
      avatar.innerHTML = `<i class="fas ${isUser ? 'fa-user' : 'fa-robot'} text-xs"></i>`;

      const bubble = document.createElement('div');
      bubble.className = `chat-bubble p-3.5 rounded-2xl text-slate-200 ${
        isUser 
          ? 'bg-emerald-950/70 border border-emerald-800/80 rounded-tr-sm text-right' 
          : 'bg-slate-800 border border-slate-700/70 rounded-tl-sm'
      }`;

      if (toolCall) {
        const badge = document.createElement('div');
        badge.className = 'inline-block mb-2 px-2 py-0.5 rounded text-[10px] font-mono bg-indigo-900/60 text-indigo-300 border border-indigo-700/50';
        badge.innerText = `⚙️ MCP Tool: ${toolCall}`;
        bubble.appendChild(badge);
      }

      const p = document.createElement('div');
      p.className = 'whitespace-pre-wrap leading-relaxed';
      p.innerText = text;
      bubble.appendChild(p);

      wrapper.appendChild(avatar);
      wrapper.appendChild(bubble);
      chatMessages.appendChild(wrapper);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function sendMessage(e) {
      if (e) e.preventDefault();
      const text = userInput.value.trim();
      if (!text) return;

      appendMessage('user', text);
      userInput.value = '';
      sendBtn.disabled = true;
      toolIndicator.classList.remove('hidden');
      toolIndicatorText.innerText = 'AI model selecting MCP tools...';

      try {
        const res = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: text,
            model: modelSelect.value,
            history: history
          })
        });

        const data = await res.json();
        toolIndicator.classList.add('hidden');

        if (data.error) {
          appendMessage('assistant', `⚠️ Error: ${data.error}`);
        } else {
          history = data.history || [];
          appendMessage('assistant', data.reply, data.tool_invoked);
        }
      } catch (err) {
        toolIndicator.classList.add('hidden');
        appendMessage('assistant', `⚠️ Network Error: ${err.message}`);
      } finally {
        sendBtn.disabled = false;
        userInput.focus();
      }
    }

    function runQuickPrompt(promptText) {
      userInput.value = promptText;
      sendMessage();
    }

    function clearChat() {
      chatMessages.innerHTML = '';
      history = [];
      appendMessage('assistant', 'Chat cleared. How can I assist you with GitHub MCP tools today?');
    }
  </script>
</body>
</html>
"""

async def homepage(request):
    return HTMLResponse(HTML_PAGE)

async def api_chat(request):
    try:
        body = await request.json()
        user_message = body.get("message", "").strip()
        selected_model = body.get("model", "openrouter/auto")
        client_history = body.get("history", [])

        if not user_message:
            return JSONResponse({"error": "Empty message"}, status_code=400)

        # Build messages payload
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        # Add past turns
        for m in client_history[-8:]:
            messages.append(m)
        messages.append({"role": "user", "content": user_message})

        # Step 1: Call model with tool definitions
        response = client.chat.completions.create(
            model=selected_model,
            messages=messages,
            tools=TOOLS_SCHEMA,
            tool_choice="auto",
        )

        choice_msg = response.choices[0].message
        tool_invoked_name = None

        if choice_msg.tool_calls:
            # Add assistant's call message
            messages.append(choice_msg)

            for tc in choice_msg.tool_calls:
                fn_name = tc.function.name
                tool_invoked_name = fn_name
                fn_args = json.loads(tc.function.arguments or "{}")
                tool_output = execute_tool_call(fn_name, fn_args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "name": fn_name,
                    "content": str(tool_output)
                })

            # Step 2: Get final conversational answer from LLM
            second_response = client.chat.completions.create(
                model=selected_model,
                messages=messages,
            )
            final_reply = second_response.choices[0].message.content
        else:
            final_reply = choice_msg.content

        # Save history for client
        updated_history = [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": final_reply}
        ]

        return JSONResponse({
            "reply": final_reply,
            "tool_invoked": tool_invoked_name,
            "history": client_history + updated_history
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

routes = [
    Route("/", homepage),
    Route("/api/chat", api_chat, methods=["POST"]),
]

app = Starlette(routes=routes)

def main():
    print("=" * 65)
    print("  GITHUB MCP SERVER — INTERACTIVE WEB INTERFACE")
    print("  MCA Minor Project | Candidate: Pranjay")
    print("=" * 65)
    print("\nStarting local web server at: http://localhost:8000")
    print("Opening browser window automatically...\n")
    try:
        webbrowser.open("http://localhost:8000")
    except Exception:
        pass
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    main()
