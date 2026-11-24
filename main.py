import asyncio
import json
import time

from tools_utils import *
from vault_agent import *


async def main():
    agents = create_agents()

    async with Client("http://localhost:8000/mcp") as mcp_client:
        tools = await get_tools(mcp_client)
        print("TOOLS FROM MCP SERVER: ")
        for tool in tools:
            print("\t- ", tool["function"]["name"])

        tasks = []
        for agent in agents:
            tasks.append(agent.act("Take 3 coins from the vault", tools, mcp_client))
        finals = await asyncio.gather(*tasks)

    for agent, final in zip(agents, finals):
        print(f"{agent.name} FINAL ANSWER : {final.content}")

asyncio.run(main()) 