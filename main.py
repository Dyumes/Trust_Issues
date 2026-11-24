from vault_agent import *

agents = create_agents()
for i in range(len(agents)):
    agent = agents[i]
    print(agent.ask(f"Respond with only your name, which is {agent.name}"))

