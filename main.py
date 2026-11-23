#CODE INSPIRED FROM https://docs.ollama.com/api/openai-compatibility
from openai import OpenAI

client = OpenAI(
    base_url='http://localhost:11434/v1/',
    api_key='ollama',  #not necessary
)

chat_completion = client.chat.completions.create(# add chat/completion to the base_url (http post at ...11434/v1/chat/completions)
    messages=[
        {
            'role': 'user',
            'content': 'Say this is a test',
        }
    ],
    model='gemma4:e2b',
)
print(chat_completion)
print(chat_completion.choices[0].message.content)
