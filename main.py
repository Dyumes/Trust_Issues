from openai import OpenAI
from vault_agent import Agent, agents

for i in range(0, len(agents)):
    agent = agents[i]
    print(agent.say(f"Respond with only your name, which is {agent.name}"))

# test1 = agents[0]
# print(test1.say(f"Respond with only your name, which is {test1.name}"))
