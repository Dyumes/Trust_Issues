import json

import anyio
from mcp import Client


#List all the tools
async def main() -> None:
    async with Client("http://localhost:8000/mcp") as client:
        result = await client.list_tools()
        for tool in result.tools:
            print(tool.name)
            print(tool.title)
            print(tool.description)
            print(tool.input_schema)


async def get_tools(client):
    """Gets the tools (asked to the MCP server) and convert
    to the openAI formaat"""

    result = await client.list_tools()
    tools = []
    for tool in result.tools:
        tools.append({
            "type" : "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.input_schema,
            }
        })
    return tools
async def execute(client, name, arguments):
    """Send the tool call to the server, return its answer"""
    result = await client.call_tool(name, json.loads(arguments))
    return result.content[0].text

if __name__ == "__main__":
    anyio.run(main)