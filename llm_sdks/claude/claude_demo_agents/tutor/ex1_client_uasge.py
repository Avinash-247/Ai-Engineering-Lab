from dotenv import load_dotenv
from helper import parse_message
from claude_agent_sdk import ClaudeAgentOptions,ClaudeSDKClient
import asyncio

async def main():
    options=ClaudeAgentOptions(
        system_prompt="you are an helpful assistant",
        setting_sources=[],
        model='claude-haiku-4-5',
        max_turns=2
    )
    async with ClaudeSDKClient(options=options) as client:
        question="my name is Avi i am from hyd"
        await client.query(question)
        async for message in client.receive_messages():
            parse_message(message)


        question="where do i live?"

        await client.query(question)
        async for message in client.receive_messages():
            parse_message(message)

if __name__== "__main__":
    load_dotenv()
    asyncio.run(main())



