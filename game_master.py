import asyncio
import time

import httpx
import yaml
from a2a.client import A2ACardResolver, ClientConfig, create_client
from a2a.helpers import new_text_message
from a2a.types import Role, SendMessageRequest

RULES = "You are playing a game called The Vault. You and other players are just guard whom have to keep a vault containing initially 100 coins. "
TIMEOUT = 20
DISCUSSION_TIME = 20

config = yaml.safe_load(open("config.yaml"))

AGENT_URLS = []
for agent in config["agents"]:
    AGENT_URLS.append(f"http://127.0.0.1:{agent["port"]}")

async def send(agent_url, text):
    async with httpx.AsyncClient() as httpx_client:
        agent_card = await A2ACardResolver(
            httpx_client=httpx_client, 
            base_url=agent_url,
        ).get_agent_card()

    # If the agent doesn't answer in the time allowed
    async with httpx.AsyncClient(timeout=TIMEOUT) as httpx_client:
        client = await create_client(
            agent=agent_card, 
            client_config=ClientConfig(streaming=False, httpx_client=httpx_client),
        )

        # Wrap the request to a A2A message
        request = SendMessageRequest(message=new_text_message(text, role=Role.ROLE_USER))

        answer = ""
        async for chunk in client.send_message(request):
            answer = chunk.task.artifacts[0].parts[0].text # Take the content of the task's response
        await client.close()
    return agent_card.name, answer

async def start_game():
    tasks = []

    for url in AGENT_URLS:
        tasks.append(send(url, RULES))
    return await asyncio.gather(*tasks)

async def broadcast_to_agents(text):
    tasks = []

    for url in AGENT_URLS:
        tasks.append(send(url, text))
    return await asyncio.gather(*tasks)

async def main():

    await start_game()

    end = time.monotonic() + DISCUSSION_TIME
    while time.monotonic() < end:
        results = await broadcast_to_agents("Discussion phase. Read the public chat, speak with your fellow guards. If the chat is empty, try to initiate (don't say that the public chat is empty)")
        for name, answer in results:
            print(f"{name}: {answer}")

    await broadcast_to_agents("The discussion is over. Do not speak anymore.")
asyncio.run(main()) 