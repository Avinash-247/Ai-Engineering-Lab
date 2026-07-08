from dotenv import load_dotenv

load_dotenv()

from langchain_chroma import Chroma
from utils import get_model_from_gcp, get_embeddings_from_gcp
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


def ingest(
        knowledge_base="./exercise",
        file_format="**/*.txt",
        persist_directory="./first_Full_Rag",
        collection_name="rag"):
    
    #1 load the doc

    loader=DirectoryLoader(
        path=knowledge_base,
        glob=file_format,
        loader_cls=TextLoader
    )

    docs=loader.load()
    print(len(docs))

    # 2. Attach document level metadata

    for doc in docs:
        filename= doc.metadata["source"].split("\\")[-1]
        doc.metadata["topic"] = filename.replace(".txt","")

    # 3. split the documents

    splitter =RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20,

    )

    chunks = splitter.split_documents(docs)

    # 4.create embeddings

    embeddings_funcation=get_embeddings_from_gcp()

    # 5 create store

    vector_store=Chroma.from_documents(
        documents=chunks,
        embedding=embeddings_funcation,
        collection_name="first",
        persist_directory=persist_directory
    )

    print(f"stored {vector_store._collection.count()} chunks in chroma")
    print("Ingestion completed")


def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

def ask(
        question,
        persist_directory="./first_Full_Rag",
        collection_name="first"):
    # 1 get vector store
    vector_store=Chroma(
        collection_name=collection_name,
        persist_directory=persist_directory,
        embedding_function=get_embeddings_from_gcp()
    )
    # 2. Create retriver
    retriever =vector_store.as_retriever()

    # 3. create a rag_prmpt

    rag_prompt=ChatPromptTemplate.from_template("""
Answer the question based only on the provided contect below
if the context dont contain enough information to anser sai i dont knao wabout please google it
                                                
                                                
Content:
    {context}
questioin:{input}
Answer: """)
    llm =get_model_from_gcp()

    # 4. retrieve docs

    retrieved_Docs=retriever.invoke(question)
    context=format_docs(retrieved_Docs)
  # 5 create chain

    chain= rag_prompt | llm |StrOutputParser()

    answer=chain.invoke({"context":context, "input": question})

    print(f'question{question}')
    print(f'Answer:{answer}')
    print(f"response{context}")

if __name__=="__main__":
    #ingest()

    question =input("enter you question: ")
    ask(question)
