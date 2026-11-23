from mcp.server.fastmcp import FastMCP, Tool
import math

#https://medium.com/@ashishpandey2062/mcp-vs-tool-calling-the-missing-standard-ai-developers-were-begging-for-c45b9273003c
server = FastMCP("my-math-server")
@server.tool()
def add(a: float, b:float) -> float:
    """Add two numebrs"""
    return a + b
@server.tool()
def sqrt(x: float) -> float:
    """Square roort"""
    return math.sqrt(x)

if __name__ == "__main__":
    server.run_stdio()