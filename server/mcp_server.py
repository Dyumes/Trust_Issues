from mcp.server import MCPServer

#TO RUN IN THE TERMINAL : uv run mcp run mcp_server.py --transport streamable-http
# will be at http://localhost:8000/mcp
mcp = MCPServer("Vault")

vault = {"money": 100}

@mcp.tool(title="Take money from the vault")
def take(amount: int) -> str:
    """Secretely take money from the vault."""

    vault["money"] -= amount
    return f"Took {amount} of money. {vault["money"]} left in the vault."

