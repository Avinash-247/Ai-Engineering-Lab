from dotenv import load_dotenv

from langchain.chat_models import init_chat_model,BaseChatModel

load_dotenv()

def get_default_model()->BaseChatModel:
    """the default chat model
    """

    model_name="google_genai:gemini-2.5-flash"
    model=init_chat_model(model=model_name)
    return model