
import asyncio

import yaml
from openai import AsyncOpenAI, OpenAI
from tools_utils import *

#Class to create an agent reading it's informations from config.yaml

config = yaml.safe_load(open("config.yaml"))

class Agent:
    def __init__(self, config):
        self.name = config["name"]
        self. model = config["model"]
        self.base_url = config["base_url"]
        self.messages = []
        self.client = AsyncOpenAI(base_url=config["base_url"], api_key=config["api_key"])

    async def ask(self, message, tools=None):
        print(self.name, f"is asked to : {message}")

        self.messages.append({
            "role": "user",
            "content": message
        })
        return await self.call(tools)
    async def call(self, tools = None):
        if tools:
            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=self.messages, 
                tools=tools
            )
        else:
            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=self.messages, 
            )
        message = completion.choices[0].message
        self.messages.append(message)
        return message

    async def act(self, message, tools, mcp_client):
        msg = await self.ask(message, tools)
        if not msg.tool_calls:
            return msg
        for call in msg.tool_calls:
            result = await execute(mcp_client, call.function.name, call.function.arguments)
            print(f"{self.name} : {call.function.name} {call.function.arguments} -> {result}")
            self.messages.append({"role" : "tool", "tool_call_id": call.id, "content": result})
        msg = await self.call(tools)

        return msg

def create_agents():
    agents : list[Agent] = []

    for agent in config["agents"]:
        agents.append(Agent(agent))

    print(f"# of agents in this session : {len(agents)}")

    return agents


 