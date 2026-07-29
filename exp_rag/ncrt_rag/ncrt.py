from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_classic.indexes import SQLRecordManager
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
loader =PyPDFLoader("./knowledge/ncrt_book.pdf")

documents = loader.load()

splitter= RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=150
)

chunks=splitter.split_documents(documents)
print(len(chunks))

print(chunks[0].metadata)

embedding=GoogleGenerativeAIEmbeddings(model="text-embedding-005")
#vector=embedding.embed_documents(
   # [chunk.page_content for chunk in chunks])
#print(vector)
vector_store=Chroma.from_documents(
    collection_name="ncrt_book",
    documents=chunks,
    embedding=embedding,
    persist_directory="./knowledge"
)
print(vector_store)

record_manager=SQLRecordManager(
    namespace="ncrt_book",
    db_url="sqlite:///record_manager.sql",
)

retriver=vector_store.as_retriever(
    search_kwargs={"k":4}
)

results=retriver.invoke(
    "what is Arithmetic Expressions ?"
)

for doc in results:
    print("="*50)
    print(doc.page_content)
    print(doc.metadata)

llm=ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


prompt = ChatPromptTemplate.from_template("""
You are an expert NCERT teacher.

Answer ONLY from the provided context.

If the answer is not present in the context,
say:

"I couldn't find this information in the NCERT book."

Context:
{context}

Question:
{question}

Answer:
""")

context="\n\n".join(
    doc.page_content for doc in results
)

final_prompt=prompt.invoke({
    "context":context,
    "question":"what is Arithmetic Expressions"
    }
)

response=llm.invoke(final_prompt)

print(response.content)

