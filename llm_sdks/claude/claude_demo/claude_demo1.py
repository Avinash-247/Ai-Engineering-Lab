from dotenv import load_dotenv
load_dotenv()

from claude_agent_sdk import query,ClaudeAgentOptions
import asyncio

async def run_query():
    options=ClaudeAgentOptions(
        model="claude-haiku-4-5"
    )
    async for message in query(
        prompt="what is the capitla of india"
    ):

        print(message)



if __name__ =="__main__":
    asyncio.run(run_query())