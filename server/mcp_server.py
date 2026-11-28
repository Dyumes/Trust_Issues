from mcp.server import MCPServer

#TO RUN IN THE TERMINAL : uv run mcp run server/mcp_server.py --transport streamable-http
# will be at http://localhost:8000/mcp
mcp = MCPServer("Vault")

vault = {"coins": 100}

@mcp.tool(title="Take money from the vault")
def take(amount: int) -> str:
    """Secretely take money from the vault."""

    vault["coins"] -= amount
    return f"Done: You took {amount} coins. {vault["coins"]} left in the vault."

