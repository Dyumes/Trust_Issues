import asyncio

import httpx
import yaml
from a2a.client import A2ACardResolver, ClientConfig, create_client
from a2a.helpers import new_text_message
from a2a.types import Role, SendMessageRequest

TIMEOUT = 20

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
            client_config=ClientConfig(streaming=False),
        )

        # Wrap the request to a A2A message
        request = SendMessageRequest(message=new_text_message(text, role=Role.ROLE_USER))

        answer = ""
        async for chunk in client.send_message(request):
            answer = chunk.task.artifacts[0].parts[0].text # Take the content of the task's response
        await client.close()
    return agent_card.name, answer

async def main():
    tasks = []

    for url in AGENT_URLS:
        tasks.append(send(url, "Take 3 coins from the vault"))
    results = await asyncio.gather(*tasks)

    for name, answer in results:
        print(f"{name}: {answer}")
asyncio.run(main()) 