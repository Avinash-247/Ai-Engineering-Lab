from langchain_google_genai import ChatGoogleGenerativeAI 
from dotenv import load_dotenv
import os
load_dotenv()
llm=ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite",
                           api_key=os.getenv("Google_Api"),)

response=llm.invoke("this is Avi")
print(response.pretty_print())