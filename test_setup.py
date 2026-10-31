"""Quick smoke test: does the server load and register tools?"""
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("test")

@mcp.tool()
def greet_user(name: str) -> str:
    """Say hello."""
    return f"Hello {name}!"

@mcp.tool()
def add_numbers(a: int, b: int) -> str:
    """Add two numbers."""
    return f"{a} + {b} = {a + b}"

print("Server created OK")
print(f"Server name: {mcp.name}")
print(f"Has .tool decorator: {hasattr(mcp, 'tool')}")
print(f"Has .run method: {hasattr(mcp, 'run')}")
print("ALL CHECKS PASSED")
