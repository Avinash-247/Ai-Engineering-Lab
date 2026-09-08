from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
load_dotenv()

from langgraph.checkpoint.memory import InMemorySaver

cfg_1= {"configurable":{"thread_id" :"classroom"}}

agent_with_memory=create_agent(
    model="google_genai:gemini-3.1-flash-lite",
    checkpointer=InMemorySaver())


response=agent_with_memory.invoke(
    {
        "messages":"this is Avi"
    },
    cfg_1
)

response=agent_with_memory.invoke(
    {
        "messages":"what is my name"
    },
    cfg_1
)
print(response)