from dotenv import load_dotenv
from langchain.chat_models import init_chat_model


load_dotenv()

def get_model():

    model=init_chat_model("google_genai:gemini-2.5-flash")

    return model

