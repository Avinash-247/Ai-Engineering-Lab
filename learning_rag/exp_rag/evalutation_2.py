
"""
Evalutation test
"""

from langchain_core.documents import Document

from langchain_community.retrievers.bm25 import BM25Retriever

from langchain_classic.retrievers.ensemble import EnsembleRetriever

from langchain_chroma import Chroma

from langchain_core.vectorstores import VectorStoreRetriever

from utils import get_embeddings_from_gcp,get_model_from_gcp

from dotenv import load_dotenv

from deepeval import evaluate

from deepeval.models import GeminiModel

from deepeval.metrics import (
    FaithfulnessMetric, ContextualPrecisionMetric,ContextualRecallMetric,
    AnswerRelevancyMetric)

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from deepeval.test_case import LLMTestCase

import os 
load_dotenv()

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
        weights=[0.5,0.5]
    )
    return hybrid_retriver

def format_doc(retrived_docs: list[Document]) -> str:
    return "\n\n".join(
        f"[page { d.metadata.get('page', "?")}] {d.page_content}" for d in retrived_docs
    )

def build_rag_chain(retriver):
    prompt=ChatPromptTemplate.from_template(
        "Answer the question using Only the Context below"
        "if the answe is not in the context ,say you don't know"
        "City the page.\n\n"
        "context{context}\n\n"
        "Questions:{question}"
    )

    llm =get_model_from_gcp()
    return (
        {"context": retriver | format_doc, "question": RunnablePassthrough()}
        |prompt
        |llm
        |StrOutputParser()
    )
def run_chain_and_build_cases(retriver,rag_chain,cases: list[dict])-> list[LLMTestCase]:
    llm_test_cases=[]

    for case in cases:
        question=case["question"]

        contexts=[d.page_content for d in retriver.invoke(question)]

        answer=rag_chain.invoke(question)
        print(f"\nQuestion: {question}\n Answer: {answer}")

        llm_test_cases.append(
            LLMTestCase(
                input=question,
                actual_output=answer,
                expected_output=case['expected'],
                retrieval_context=contexts

            )
        )
    return llm_test_cases
def evaluate_chain(llm_test_cases: list[LLMTestCase]):
    judge=GeminiModel(
        model="gemini-2.5-flash-lite",
        use_vertexai=True,
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION"),
        temperature=0
    )
    metrics=[
        ContextualPrecisionMetric(threshold=0.7,model=judge),
        ContextualRecallMetric(threshold=0.7,model=judge),
        FaithfulnessMetric(threshold=0.7,model=judge),
        AnswerRelevancyMetric(threshold=0.7,model=judge)
    ]

    return evaluate(test_cases=llm_test_cases,metrics=metrics)

def main():
    cases=[
        {
            "question": "what does it mean to split some thing into equal parts?",
            "expected" : "A fration is what you get when you divide something"
        },
        {
            "question":"what is the fromula does the exercise 4.3?",
            "expected" : "it's the formula that you already know"
        }
    ]

    documents=build_documents()

    dense_retriver=build_dense_retriver(documents)
    sparse_retriver=build_sparse_retriver(documents)
    retriver = build_hybrid_retriver(
        dense_retriver,sparse_retriver
    )
    rag_chain=build_rag_chain(retriver)
    llm_test_cases=run_chain_and_build_cases(retriver,rag_chain,cases)

    results=evaluate_chain(llm_test_cases)
    print(results)


if __name__=="__main__":
    main()