
import asyncio

import yaml
from openai import AsyncOpenAI, OpenAI

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
    # def ask(self, message):
        # print(self.name, f"is asking to : {message}")
        # chat_completion = await self.client.chat.completions.create(
        #     model=self.model, 
        #     messages=[
        #         {
        #             'role': 'user',
        #             'content': message,
        #         }

        #     ]
        # )
        # answer = chat_completion.choices[0].message.content
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




def create_agents():
    agents : list[Agent] = []

    for agent in config["agents"]:
        agents.append(Agent(agent))

    print(f"# of agents in this session : {len(agents)}")

    return agents


 