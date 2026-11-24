import asyncio
import json
import time

from tools_utils import *
from vault_agent import *


async def main():
    agents = create_agents()
    tasks = []

    for agent in agents:
        # results.append(agent.ask("Count from 1 to 100 separated by a coma"))
        tasks.append(agent.ask("Take 3 coins from the vault.", tools=TOOLS))
        
    messages = await asyncio.gather(*tasks)

    for agent, message in zip(agents, messages):
        if not message.tool_calls:
            print(f"{agent.name} => NO TOOL CALL -> {message.content}")
            continue
        call = message.tool_calls[0]
        
        arguments = json.loads(call.function.arguments)
        if call.function.name == "take":
            result = take(arguments["amount"])
        else:
            result = f"DONT KNWO THIS TOOL: {call.function.name}"
        print(f"{agent.name} : {call.function.name} {call.function.arguments}")
        final = await agent.call(tools=TOOLS)
        print(f"{agent.name} : {arguments} -> {result} -> {final.content}")
    # start = time.perf_counter()
    # answers = await asyncio.gather(*results)
    # print(f"TOTAL: {time.perf_counter() - start:.1f}s")
    # for agent, answer in zip(agents, answers):
    #     print(agent.name, " -> ", answer)
asyncio.run(main()) 