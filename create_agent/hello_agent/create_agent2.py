from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage,AIMessage,SystemMessage
from dotenv import load_dotenv
import os
load_dotenv()

model=init_chat_model(model="gemini-3.5-flash-lite",
                      model_provider='google_genai',
                      api_key=os.getenv("Google_Api"))
message=[
    HumanMessage("this is Avi"),
    HumanMessage("what is Capital of India"),
    HumanMessage("what is My name"),
    SystemMessage("you just suppose say the Answer dont give me unnecessary conent"),
    
]
response=model.invoke(message)
print(response.pretty_print())