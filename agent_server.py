import sys

import uvicorn
from a2a.helpers import (
    get_message_text,
    new_task_from_user_message,
    new_text_message,
    new_text_part,
)
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from a2a.server.tasks import InMemoryTaskStore, TaskUpdater
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentInterface,
    AgentSkill,
    TaskState,
)
from mcp import Client
from starlette.applications import Starlette
from tools_utils import get_tools
from vault_agent import Agent, config

MCP_URL = "http://localhost:8000/mcp"

# Wrapper around the actual vault agent so it becomes a "mini-server"
#HEAVILY INSPIRED FROM : https://github.com/a2aproject/a2a-samples/tree/main/samples/python/agents/helloworld
class VaultAgentExecutor(AgentExecutor):
    def __init__(self,agent):
        self.agent = agent

    async def execute(self, context: RequestContext, event_queue: EventQueue):
        #Collect a task from the request context
        if context.current_task:
            task = context.current_tasks
        else:
            # No task -> create one and add it to event queue
            task = new_task_from_user_message(context.message)
            await event_queue.enqueue_event(task)

        # Update the task status
        task_updater = TaskUpdater(
            event_queue=event_queue, 
            task_id = task.id, 
            context_id=task.context_id,
        )
        await task_updater.update_status(
            state=TaskState.TASK_STATE_WORKING, 
            message=new_text_message("THINKING..."),
        )

        # Collect the request from the content
        text = get_message_text(context.message)
        # Connect to MCP to get the different tools and act for the LLM agent
        async with Client(MCP_URL) as mcp_client:
            tools = await get_tools(mcp_client)
            reply = await self.agent.act(text, tools, mcp_client)

        # Just for when the model decided to say absolutely NOTHING
        answer = reply.content
        if not answer:
            answer = "(no text answer)"

        # Artifact = output gen by the agent during the task
        # So we add the response as an artifact to eventQueue
        await task_updater.add_artifact(parts=[new_text_part(text=answer, media_type="text/plain")])
        # And finally update the status to completed
        await task_updater.update_status(state=TaskState.TASK_STATE_COMPLETED, message=new_text_message("DONE."))

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        # NO CANCEL FOR NOW, JUST NEEDED BECAUSE IT'S ABSTRACT
        raise NotImplementedError("CANCEL NOT SUPPORTED")
    
def main (idx: int):
    agent_config = config["agents"][idx]
    agent = Agent(agent_config)
    port = agent_config["port"]



    # Card that allows clients to discover agent capabilites
    agent_card = AgentCard(
        name=agent.name,
        description=f"Agent using {agent.model}",
        version="0.0.1",
        # Default media types for its interactions
        default_input_modes=["text/plain"],
        default_output_modes=["text/plain"],
        capabilities=AgentCapabilities(streaming=False), # Features, not use for now ? TODO: check what it really means
        # Endpoits & protocols where the service can be reached
        supported_interfaces=[
            AgentInterface(
                protocol_binding="JSONRPC", 
                url=f"http://127.0.0.1:{port}",
                protocol_version="1.0")
        ],
        # TODO: see how the skill reeally affect the agent
        skills=[AgentSkill(
            id="play", 
            name="Play The Vault", 
            description="Plays he game",
            tags=["game"]
            )],
    )
    # Process incoming requests and manage tasks
    request_handler = DefaultRequestHandler(
        # Handles execution of the client requests
        agent_executor=VaultAgentExecutor(agent), 
        # Store + manage task
        task_store=InMemoryTaskStore(),
        # Unauthenticateed users
        agent_card=agent_card,
        )
    # Creates the route for the A2A server
    routes = []
    routes.extend(create_agent_card_routes(agent_card))
    routes.extend(create_jsonrpc_routes(request_handler, "/"))

    # Run the app (created a web app with defined routes)
    uvicorn.run(Starlette(routes=routes), host="127.0.0.1", port=port)

if __name__ == "__main__":
    main(idx=int(sys.argv[1]))
