from claude_agent_sdk import ClaudeAgentOptions,query
from dotenv import load_dotenv

from helper import base_options,parse_message

from typing import Literal
import asyncio

load_dotenv()
Tone_Dict={
    "Beginner":"you are a tutor explain me a topic which very clear in simpleform easy to remember",
    "Revision":"you are an tutor help me to revise, i have an exam",
    "Detailed":"you are an tutor help me to explian in 2 lined by 80/20 rule"
    }

async def conversation(
        tone:Literal["Detailed","Revision","Beginner"],
        question:str="what is the data"
    ):
    choose_tone={
        "system_prompt":Tone_Dict.get(tone,"Beginner")
    }
    options=base_options(**choose_tone)
    count=0
    async for message in query(prompt=question,options=options):
        count+=1
        print(f"count:{count}:{type(message)}")
        parse_message(message=message)


async def ask_questions():
    question=input("Enter you question: ")
    tone=input("choose one option among this Detailed,Revision,Beginner: ")
    await conversation(tone,question)

if __name__=="__main__":
    asyncio.run(ask_questions())