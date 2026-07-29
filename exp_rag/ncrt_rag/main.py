'''def main():
    print("Hello from ncrt-rag!")


if __name__ == "__main__":
    main()'''

'''from langchain_google_genai import GoogleGenerativeAIEmbeddings
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

print(response.content)'''