TOOLS = [
    {
        "type" : "function",
        "function": {
            "name" : "take",
            "description" : "Secretely take coins from the shared vault.",
            "parameters": {
                "type": "object",
                "properties": {"amount" : {"type": "integer", "description" : "Number of coins to take"}},
                "required": ["amount"],
            }
        }
    }
]


vault = 100

def take(amount):
    global vault
    vault -= amount
    print(f"Took {amount}, {vault} left in the vault")