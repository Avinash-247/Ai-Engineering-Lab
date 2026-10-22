import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from calculator_agnet.agent import root_agent
from dotenv import load_dotenv

load_dotenv()


App_name="calculator_app"
User_Id="user_1"
Session_Id="Session_1"

async def main():
    session_service=InMemorySessionService()

    await session_service.create_session(
        app_name=App_name,
        user_id=User_Id,
        session_id=Session_Id,
    )

    runner=Runner(
        agent=root_agent,
        app_name=App_name,
        session_service=session_service,
    )

    message=types.Content(
        role="user",
        parts=[types.Part(text="What is 25 add 4?")]

    )

    async for event in runner.run_async(
        user_id=User_Id,
        session_id=Session_Id,
        new_message=message,
    ):
        print("Author:",event.author)
        print("Event content:", event.content)

        if event.is_final_response():
            print("final_answer: ",event.content.parts[0].text)


if __name__=="__main__":
    asyncio.run(main())