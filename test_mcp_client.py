import asyncio
import sys
import os
from fastmcp import Client
from fastmcp.client.transports import StdioTransport

async def main():
    # Get city from command line argument or prompt user
    if len(sys.argv) > 1:
        city = sys.argv[1]
    else:
        city = input("Enter city name: ")
    
    # Pass environment variables to the server subprocess
    required_vars = ["OPENWEATHER_API_KEY"]
    env = {
        var: os.environ[var] 
        for var in required_vars 
        if var in os.environ
    }
    
    transport = StdioTransport(
        command="python3",
        args=["server.py"],
        env=env
    )
    client = Client(transport)
    
    # Connect to the server
    async with client:
        # List available tools
        tools = await client.list_tools()
        print("Available tools:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        
        print("\n" + "="*50 + "\n")
        
        # Call the current weather tool
        result = await client.call_tool(
            "get_current_weather", 
            {"city": city}
        )
        print(f"Weather result:\n\n {result}")

if __name__ == "__main__":
    asyncio.run(main())
