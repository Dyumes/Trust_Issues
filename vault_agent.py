
import asyncio
import json
import random
from datetime import datetime

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
        self.log_file = f"logs/{self.name}.jsonl"
        open(self.log_file, "w").close()
        self.client = AsyncOpenAI(base_url=config["base_url"], api_key=config["api_key"])

    async def ask(self, message, tools=None):
        print(self.name, f"is asked to : {message}")

        self.messages.append({
            "role": "user",
            "content": message
        })

        self.log({"type": "asked", "content": message})
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

        requested = []
        if message.tool_calls:
            for tool_call in message.tool_calls:
                requested.append({"tool": tool_call.function.name, "args": tool_call.function.arguments})
        self.log({"type": "answered", "content": message.content, "tool_calls": requested})
        return message

    async def act(self, message, tools, mcp_client):
        msg = await self.ask(message, tools)
        if not msg.tool_calls:
            return msg
        for call in msg.tool_calls:
            result = await execute(mcp_client, call.function.name, call.function.arguments)
            print(f"{self.name} : {call.function.name} {call.function.arguments} -> {result}")
            self.messages.append({"role" : "tool", "tool_call_id": call.id, "content": result})
            self.log({"type": "tool_result", "tool": call.function.name, "result": result})  # le résultat

        msg = await self.call(tools)

        return msg

    def log(self, event):
        event["time"] = datetime.now().isoformat(timespec="milliseconds")

        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(json.dumps(event) + "\n")



def create_agents():
    agents : list[Agent] = []

    for agent in config["agents"]:
        agents.append(Agent(agent))
  
    print(f"# of agents in this session : {len(agents)}")

    return agents


 