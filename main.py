import asyncio

from vault_agent import *


async def main():
    agents = create_agents()
    asks = []
    for i in range(len(agents)):
        agent = agents[i]
        asks.append(agent.ask(f"Respond with only your name, which is {agent.name}"))
        # agent = agents[i]
        # print(await agent.ask(f"Respond with only your name, which is {agent.name}"))
    answers = await asyncio.gather(*asks)
    for agent, answer in zip(agents, answers):
        print(agent.name, " -> ", answer)
asyncio.run(main()) 