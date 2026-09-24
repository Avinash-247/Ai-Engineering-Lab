"""dense vs sprase vs hybrid"""


from langchain_core.documents import Document

from langchain_community.retrievers.bm25 import BM25Retriever

from langchain_classic.retrievers.ensemble import EnsembleRetriever

from langchain_chroma import Chroma

from langchain_core.vectorstores import VectorStoreRetriever

from utils import get_embeddings_from_gcp

from dotenv import load_dotenv

def build_documents() -> list[Document]:
    raw_chunks = [
        {
            "text": (
                "A fraction represents a part of a whole. "
                "When we divide a pizza into 4 equal slices and take 1, "
                "we have 1/4 of the pizza."
            ),
            "metadata": {"chapter": "fraction", "page": 13},
        },
        {
            "text": (
                "Decimals are another way to represent fractions. "
                "For example, 0.25 is the decimal form of 1/4."
            ),
            "metadata": {"chapter": "decimal", "page": 27},
        },
        {
            "text": (
                "Percentages express fractions with a denominator of 100. "
                "For instance, 25% is equivalent to 25/100 or 1/4."
            ),
            "metadata": {"chapter": "percentage", "page": 45},
        },
    ]

    return [Document(page_content=chunk["text"],metadata=chunk["metadata"])
        for chunk in raw_chunks]

def build_dense_retriver(documents: list[Document])-> VectorStoreRetriever:

    embedding_model = get_embeddings_from_gcp()

    vectorstore=Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        collection_name="retriver_demo"
    )
     
    dense_retriver =vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k":3}
    )
    return dense_retriver

def build_sparse_retriver(documents: list[Document]):

    sparse_retriver=BM25Retriever.from_documents(documents)
    sparse_retriver.k=3
    return sparse_retriver

def build_hybrid_retriver(dense_retriver, sparse_retriver) -> EnsembleRetriever:
    hybrid_retriver=EnsembleRetriever(
        retrievers=[dense_retriver, sparse_retriver],
        weight=[0.5,0.5]
    )
    return hybrid_retriver

def run_comparision():

    documents=build_documents()
    dense_retriver=build_dense_retriver(documents)
    sparse_retriver=build_sparse_retriver(documents)
    hybrid_retriver=build_hybrid_retriver(dense_retriver,sparse_retriver)

    querys=[
        "what does it mean to split some thing into equal portions",
        "Exercise 4.3 triangle"
    ]

    for query in querys:

        print(f"\n{'=' * 60}\nquery:{query}\n{"=" *60}")

        print("--Dense_")

        for doc in dense_retriver.invoke(query):
            print(doc.page_content)
        
        print("--sparse")

        for doc in sparse_retriver.invoke(query):
            print(doc.page_content)

        print("hybrid")

        for doc in hybrid_retriver.invoke(query):
            print(doc.page_content)

if __name__=="__main__":
    run_comparision()