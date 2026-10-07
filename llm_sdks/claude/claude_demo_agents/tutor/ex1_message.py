from dotenv import load_dotenv

import os

from claude_agent_sdk import query, ClaudeAgentOptions,Message
import asyncio
from  helper import base_options,parse_message

model_name="claude-haiku-4-5"

async def initiate_conversation()-> Message:
    options=base_options()
    question="what is difference b/w functiona and generator"
    count= 0
    async for message in query(prompt=question,options=options):
        count+=1
        print(f"{count}: {type(message)}")
        parse_message(message=message)








if __name__=="__main__":


    load_dotenv()
    asyncio.run(initiate_conversation())