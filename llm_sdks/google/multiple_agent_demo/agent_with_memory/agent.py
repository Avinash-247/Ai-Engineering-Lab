from google.adk.agents.llm_agent import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

import asyncio

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
)

session_service=InMemorySessionService()

runner=Runner(
    agent=root_agent,
    app_name="helping_agent",
    session_service=session_service,
)

# async def main():
#     session=await session_service.create_session(
#         state={},
#         user_id="Avi_1"
#     )

# if __name__=="__main__":
#     asyncio.run(main())

# print(runner.agent.name)