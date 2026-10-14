from claude_agent_sdk import (
    ClaudeAgentOptions,ClaudeSDKClient,
    InMemorySessionStore,SessionStore)
from dotenv import load_dotenv
from helper import parse_message
import asyncio
from session_storage import SessionStorage
# Session_Store=InMemorySessionStore()
Storage=SessionStorage("database.db")
# Storage=SessionStore("database.db")


async def main():
    user_id=input("what is your user ID").strip()

    if not user_id:
        print("user ID cannot be empty")
        return 
    session_id=Storage.get_session(user_id)

    if session_id is None:
        print("created new user")
        Storage.create_user(user_id)
    else:
        print(f"saved session_id{session_id}")

    options=ClaudeAgentOptions(
        system_prompt="you are a helpful tutor Assistent",
        model="claude-haiku-4-5",
        max_turns=2,
        #session_id=
        setting_sources=[],
        session_store=Storage,
    )
    async with ClaudeSDKClient(options=options) as client:

        while True:
            question=input("enter you query: ").strip()

            if question.lower() in {"exit","quit"}:
                break
            if not question:
                continue
            await client.query(question)

            async for message in client.receive_messages():
                parse_message(message)

        # question="this is Avi"
        # await client.query(question)
        # async for message in client.receive_messages():
        #     parse_message(message)

        
        # question="what's my name"
        # await client.query(question)
        # async for message in client.receive_messages():
        #     parse_message(message)


if __name__=="__main__":
    load_dotenv()
    asyncio.run(main())
