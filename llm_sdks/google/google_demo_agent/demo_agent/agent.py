from google.adk.agents.llm_agent import Agent
from dotenv import load_dotenv

load_dotenv()

def get_current_time(city:str)->dict:
    return {"state":"Tamilnadu","city":city,"time":"4:00AM"}


root_agent=Agent(
    name="time",
    model="gemini-3.5-flash",
    description="tells the current time in chennai ",
    instruction="You are a helpful assistant. Use the get_current_time tool when the user asks for the time.",
    tools=[get_current_time]
)

