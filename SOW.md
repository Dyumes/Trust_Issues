# Statements of Work

### 23.11.2026 -> 25.11.2026
---

1) Deploy ollama on laptop
- Install ollama
- Pull a model (for now gemma4:e2b, will change to gemma4:e2b-it-qat)
- Configure context size (on server-side by OLLAMA_CONTEXT_LENGTH) and parallelization
- Verification with ollama ps
- Test parallel sessions and get results
- Test tool calling with gemma4:e2b-it-qt

2) Connect to the model from Python
- Python project environement 
- Model called through the OpenAI API through /v1/chat/completions
- Configurable base URL, model name and API key in config.yaml
- Run sequentially several agents on the same model 
- History per agent

    Docs used :

    https://ollama.com/library/gemma4:e2b

    https://docs.ollama.com/

    https://ollamaherd.com/guides/ollama-concurrent-requests

    https://developers.openai.com/api/reference/python

    https://docs.python.org/3/library/asyncio-task.html#asyncio.gather

#### Model selection ; GPU = RTX 4060 LAPTOP 8GB (available ~6.9GB)

SERVER SETTINGS : 
- OLLAMA_CONTEXT_LENGTH = 16384
- OLLAMA_NUM_PARALLEL = 5
- OLLAMA_FLASH_ATTENTION = 1
- OLLAMA_KV_CACHE_TYPE = q8_0

| Model | Context Size | Parallel | Size | Processor | Good to work (all on gpu) | 1 agent : "Count from 1 to 100 separated by a coma" | Token/s |
| -- | -- | -- | -- | -- | -- | -- | -- |
| qwen3.5:9b| 16384 | 5 | 8.4GB | 34%/66% CPU/GPU | No | 102.8s | 13.8 |
| qwen3.5:9b| 8192 | 5 | 7.3GB | 22%/78% CPU/GPU | No | 47.1s | - | 
| qwen3.5:9b| 4096 | 5 | 6.7GB | 16%/84% CPU/GPU | No | 97.2s | - | 
| qwen3.5:4b| 16384 | 5 | 5 GB | 100% GPU | Yes | 66.7s | 67.9|
| qwen3.5:4b| 8192 | 5 | 4.4 GB | 100% GPU | Yes | 64.9s | - |
| qwen3.5:4b| 4096 | 5 | 3.7 GB | 100% GPU | Yes | 43.9s | - |
| gemma4:e4b-it-qat | 16384 | 5 | 3.5GB | 100% GPU | Yes | 18.4s | 65.7 |
| gemma4:e4b-it-qat | 8192 | 5 | 3.4GB | 100% GPU | Yes | 16.2s | - |
| gemma4:e4b-it-qat | 4096 | 5 | 3.3GB | 100% GPU | Yes | 17.2s | - |
| gemma4:e2b-it-qat | 16384 | 5 | 1.9GB | 100% GPU | Yes | 11.4s | 119.4 | 
| gemma4:e2b-it-qat | 8192 | 5 | 1.9GB | 100% GPU | Yes | 12.1s | - |
| gemma4:e2b-it-qat | 4096 | 5 | 1.9GB | 100% GPU | Yes | 15.4s | - |

3) Connect MCP -> to one model
- Basic MCP server with one tool
- Connect one agent

    Docs used:

    https://medium.com/@ashishpandey2062/mcp-vs-tool-calling-the-missing-standard-ai-developers-were-begging-for-c45b9273003c

    https://py.sdk.modelcontextprotocol.io/client/

### 26.11.2026 -> 30.11.2026
---
4) Connect A2A (basic rex exchanges)

5) Game Context (rules, scalable on number of player) / Framework

Docs used :

https://github.com/a2aproject/a2a-python

https://github.com/a2aproject/a2a-samples


## TO TEST
- models : how 2B, how 2B with some 4B 
how to compose the memory 

- memory:
->cross-round with isolated games (doesnt remmeber wehat happen)
->cross-games with memory of the games
-> find some ways to keep good info 

- communication is:
-> peer 2 peer + chat
-> chat

have some interface to show all of these (after all the backend)
avidio, adem

on a seperate page -> stats

no matter the interface (Web, QT, ...)


In this file -> everything that has bveen done + precise


