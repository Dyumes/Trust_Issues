import asyncio

from vault_agent import *


async def main():
    agents = create_agents()
    for i in range(len(agents)):
        agent = agents[i]
        print(await agent.ask(f"Respond with only your name, which is {agent.name}"))

asyncio.run(main())