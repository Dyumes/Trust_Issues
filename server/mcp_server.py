import json
from datetime import datetime

from mcp.server import MCPServer
from mcp.server.mcpserver import Context

#TO RUN IN THE TERMINAL : uv run mcp run server/mcp_server.py --transport streamable-http
# will be at http://localhost:8000/mcp
mcp = MCPServer("Vault")

vault = {"coins": 100}
public_chat = []

def log_chat(player, message):
    event = {
        "time": datetime.now().isoformat(timespec="milliseconds"), 
        "player": player, 
        "message": message
    }
    with open("logs/chat.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

@mcp.tool(title="Take money from the vault")
def take(amount: int) -> str:
    """Secretely take money from the vault."""

    vault["coins"] -= amount
    return f"Done: You took {amount} coins. {vault["coins"]} left in the vault."

@mcp.tool(title="Talk in the public chat")
def say(message: str, context: Context) -> str:
    """Say something to the public chat"""
    player = context.session.client_params.client_info.name
    public_chat.append(f"{player}: {message}")
    print(f"[PUBLIC CHAT] {player}: {message}")
    log_chat(player, message)
    return "Msg posted in the public chat"

@mcp.tool(title="Read everything that has been said in the public chat")
def read_chat() -> str:
    """Read the public chat where all players can talk"""
    if not public_chat:
        return "(CHAT IS EMPTY)"
    return "\n".join(public_chat)

