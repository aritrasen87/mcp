## multiserver_client.py

import asyncio
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4o-mini")

from dotenv import load_dotenv
os.environ['TAVILY_API_KEY'] = os.environ.get("TAVILY_API_KEY")

async def main():

        current_dir = os.path.dirname(os.path.abspath(__file__))
        math_server_path = os.path.join(current_dir, "math_server.py")

        async with MultiServerMCPClient(
            {
                "math": {
                    "command": "python",
                    # Make sure to update to the full absolute path to your math_server.py file
                    "args": [math_server_path],
                    "transport": "stdio",
                },
                "WebSearch": {
                    # make sure you start your WebSearch server on port 8000
                    "url": "http://localhost:8000/sse",
                    "transport": "sse",
                }
            }
        ) as client:
            agent = create_react_agent(model, client.get_tools())
            math_response = await agent.ainvoke({"messages": "what's (3 + 5) x 12?"})
            web_response = await agent.ainvoke({"messages": "what is the weather in Kolkata?"})
            print('1st Reponse:',math_response['messages'][-1].content)
            print('2nd Reponse:',web_response['messages'][-1].content)

if __name__ == "__main__":
    asyncio.run(main())