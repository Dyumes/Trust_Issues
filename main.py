import asyncio
import time

from vault_agent import *


async def main():
    agents = create_agents()
    asks = []
    # for agent in agents:
    #     asks.append(agent.ask("Count from 1 to 100 separated by a coma"))
      
    # start = time.perf_counter()
    answers = await asyncio.gather(*asks)
    # print(f"TOTAL: {time.perf_counter() - start:.1f}s")
    for agent, answer in zip(agents, answers):
        print(agent.name, " -> ", answer)
asyncio.run(main()) 