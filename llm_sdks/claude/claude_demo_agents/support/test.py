from dotenv import load_dotenv
from helper import parse_message
from claude_agent_sdk import (
    ClaudeAgentOptions,query,ClaudeSDKClient,
    InMemorySessionStore,SessionStore)
import asyncio


#Session_Store=InMemorySessionStore()
#Session_Store=SessionStore("database.db")

async def main():
    options=ClaudeAgentOptions(
        system_prompt="you are an helpful assistant",
        setting_sources=[],
        model='claude-haiku-4-5',
        max_turns=20,
        #session_store=Session_Store,

    )
    question="what is my name"
    async for message in query(prompt=question,options=options):
        parse_message(message)


if __name__== "__main__":
    load_dotenv()
    asyncio.run(main())



