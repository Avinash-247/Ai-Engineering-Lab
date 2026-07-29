from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_classic.indexes import SQLRecordManager
from dotenv import load_dotenv


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
vector=embedding.embed_documents(
    [chunk.page_content for chunk in chunks]
    )
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
    db_url="sql:///record_manager.sql",
    vector_store=vector_store
)
