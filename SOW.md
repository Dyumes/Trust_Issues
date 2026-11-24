# Statements of Work

### 23.11.2026 -> 25.11.2026

1) Deploy ollama on laptop
- Install ollama
- Pull a model (for now gemma4:e2b, will change to gemma4:e2b-it-qat)
- Configure context size (on server-side by OLLAMA_CONTEXT_LENGTH) and parallelization
- Verification with ollama ps
- TODO - Test parallel sessions and get results
- TODO - Test tool calling with gemma4:e2b-it-qt

2) Connect to the model from Python
- Python project environement 
- Model called through the OpenAI API through /v1/chat/completions
- Configurable base URL, model name and API key in config.yaml
- Run sequentially several agents on the same model 
- TODO - History per agent
- TODO - MAYBE - Add a sys prompt per agent ? (role: guard /Thief/ Auditor) 

    Docs used :

    https://ollama.com/library/gemma4:e2b

    https://docs.ollama.com/

    https://ollamaherd.com/guides/ollama-concurrent-requests

    https://developers.openai.com/api/reference/python

3) Connect MCP -> to one model
- TODO - Basic MCP server with one tool
- TODO - Connect one agent

    Docs used:

    https://medium.com/@ashishpandey2062/mcp-vs-tool-calling-the-missing-standard-ai-developers-were-begging-for-c45b9273003c

3) Connect A2A (basic rex exchanges)
4) Game Context (rules, scalable on number of player) / Framework