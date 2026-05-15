import asyncio
import os
from agentapi.agent.agent import Agent
from agentapi.agent.tools import tool

# Set your API key for testing (Replace with a real key if you have one)
# If you don't have one, the code will fail with an Auth error, 
# but that STILL proves your routing and provider initialization worked!
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-api03-YOUR-KEY-HERE"

@tool
def get_weather(location: str) -> str:
    """Get the current weather for a location."""
    print(f"\n[TOOL EXECUTED] Getting weather for: {location}")
    return f"The weather in {location} is 72°F and sunny."

async def main():
    print("Initializing Anthropic Agent...")
    try:
        agent = Agent(
            system_prompt="You are a helpful assistant. Use tools if necessary.",
            provider="anthropic",
            tools=[get_weather]
        )
        print("✅ Agent initialized successfully with Anthropic provider!")

        print("\nSending message: 'What is the weather in San Francisco?'")
        response = await agent.run("What is the weather in San Francisco?")
        
        print("\n--- Final Response ---")
        print(response)
        
    except Exception as e:
        print(f"\n❌ Error encountered: {e}")

if __name__ == "__main__":
    asyncio.run(main())