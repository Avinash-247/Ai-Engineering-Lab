from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_classic.indexes import SQLRecordManager
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

from deepeval.metrics import (
    FaithfulnessMetric,
    AnswerRelevancyMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    ContextualRelevancyMetric
)
from deepeval import evaluate
from deepeval.test_case import LLMTestCase

from main import GeminiModel

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
question="what is Arithmetic Expressions"
results=retriver.invoke(question)

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

retrieval_context = [
    doc.page_content
    for doc in results
]

context = "\n\n".join(retrieval_context)

final_prompt=prompt.invoke({
    "context":context,
    "question":question
    }
)

response=llm.invoke(final_prompt)

#print(response.content)


#from here i am testing how all kind of test evals are 
# working so for that purpose i am usinf more than 
# required deepevals its just for my experment
google_model=GeminiModel()
test_case=LLMTestCase(
    input=question,
    actual_output=response.content,
    expected_output=(
        "Arithmetic expressions are mathematical expressions "
        "made using numbers and arithmetic operators."
    ),

    retrieval_context=retrieval_context
)

faithfulness=FaithfulnessMetric(model=google_model)
evaluate(
    test_cases=[test_case],
    metrics=[faithfulness],
)

answer_releveancy=AnswerRelevancyMetric(model=google_model)
evaluate(
    test_cases=[test_case],
    metrics=[answer_releveancy],
)

context_presesion= ContextualPrecisionMetric(model=google_model)
evaluate(
    test_cases=[test_case],
    metrics=[context_presesion]
)

context_recall=ContextualRecallMetric(model=google_model)

evaluate(
    test_cases=[test_case],
    metrics=[context_recall]
)

context_relevancy=ContextualRelevancyMetric(model=google_model)

evaluate(
    test_cases=[test_case],
    metrics=[context_relevancy]
)

