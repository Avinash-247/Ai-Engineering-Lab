from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
def get_model_from_gcp(model_name:str="gemini-2.5-flash"):
    return ChatGoogleGenerativeAI(model=model_name)