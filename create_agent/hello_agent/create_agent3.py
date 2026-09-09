from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
import os
load_dotenv()
model=init_chat_model(model="google_genai:gemini-3.5-flash-lite",
                        api_key=os.getenv("Google_Api")
                    )
agent=create_agent(
    model=model,
    tools=[]
    )
response=agent.invoke({
    "messages":["what is my name"]
})
print(response )
