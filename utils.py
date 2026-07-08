from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()
def get_model_from_gcp(model_name:str="gemini-2.5-flash"):
    return ChatGoogleGenerativeAI(model=model_name)

from langchain_google_genai import GoogleGenerativeAIEmbeddings

def get_embeddings_from_gcp(model_name:str ="text-embedding-005")->GoogleGenerativeAIEmbeddings:
    """this method returns a chat model from gcp
    
    Args :
        model_name (str,optional): _desciption_. Default to "text-embedding-005"
        """
    return GoogleGenerativeAIEmbeddings(
        model=model_name,
    )