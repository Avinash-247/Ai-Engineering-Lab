'''def main():
    print("Hello from ncrt-rag!")


if __name__ == "__main__":
    main()'''
# this code is usesd for test the embeddings Api is veorking are not
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="text-embedding-005")
vector = embeddings.embed_query("hello, world!")
print(vector[:5])
import os
print(os.getenv("GOOGLE_API_KEY"))

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

response = llm.invoke("Say hello")

print(response.content)



#this code is for evalutation test 
'''from deepeval.models import DeepEvalBaseLLM
from langchain_google_genai import ChatGoogleGenerativeAI

class GeminiModel(DeepEvalBaseLLM):

    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0
        )

    def load_model(self):
        return self.model

    def generate(self, prompt: str) -> str:
        return self.model.invoke(prompt).content

    async def a_generate(self, prompt: str) -> str:
        response = await self.model.ainvoke(prompt)
        return response.content

    def get_model_name(self):
        return "gemini-2.5-flash"'''