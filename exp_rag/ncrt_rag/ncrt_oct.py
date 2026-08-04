import fitz
import os

from PIL import Image
import io
import numpy as np

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

doc=fitz.open("knowledge/ncrt_book.pdf")
output_folder="knowledge/extracted_images"
os.makedirs(output_folder, exist_ok=True)
from dotenv import load_dotenv
load_dotenv()
# here we are facing few blank images 
# so that why i have some up with this idea
'''MIN_WIDTH = 500
MIN_HEIGHT = 500
BLANK_STD_THRESHOLD = 50

def is_blank_or_tiny(image_bytes, ext):
    try:
        img = Image.open(io.BytesIO(image_bytes))

        if img.width < MIN_WIDTH or img.height < MIN_HEIGHT:
            return True
        gray = img.convert("L")
        arr = np.array(gray)

        if arr.std() < BLANK_STD_THRESHOLD:
            return True

        return False
    except Exception as e:
        print(f"could not check image: {e}")
        return True'''
#text Extraction
loader=PyPDFLoader("knowledge/ncrt_book.pdf")
text_output_folder="knowledge/entracted_text"
os.makedirs(text_output_folder,exist_ok=True)
document=loader.load()
text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=50,
    separators=['\n\n','\n',"."," ",""],
    length_function=len
)
chunk=text_splitter.split_documents(document)
#print(f"totsl:{len(chunk)}")
#print(chunk[0].page_content)
#print(chunk[0].metadata)
for page_numbers in range(len(document)):
    page=document[page_numbers]
    text=page.page_content
    text_file_name=f"{page_numbers}.txt"
    text_file_path=os.path.join(text_output_folder,text_file_name)

    with open(text_file_path, "w", encoding="utf-8") as file:
        file.write(text)

    print(f"saved:{text_file_name}")

embedding=GoogleGenerativeAIEmbeddings(
    model="text-embedding-005"
)

persist_directory="knowledge2/chroma_db"

vectorstore=Chroma.from_documents(
    collection_name="ncrt_book",
    documents=chunk,
    embedding=embedding,
    persist_directory=persist_directory,
)
print(len(chunk),persist_directory)

llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
prompt=ChatPromptTemplate.from_template(
    '''you are an expert NCRT TEACHER.
    Answer ONly from the provided context.
    if the answer is not present in that context ,
    say :
    "I couldn't find this information in the nCER BOOK.
    
    context:
    {context}
    Question:
    {question}
    Answer:
    '''
)

def ask_question(question,k=4):
    retriver=vectorstore.as_retriever(search_kwargs={"k":k})
    results=retriver.invoke(question)

    context="\n\n".join(docs.page_content for docs in results)

    final_prompt=prompt.invoke(context, question,)

    response=llm.invoke(final_prompt)

    return{
        "answer":response.content,
        "sources": results
    }

def chat_loop():
    print("NCRT RAG ASSISTANT-type exit to quit\n")

    while True:
        question=input("Ask a question:").strip()

        if question.lower() in ("exit", "quit","q"):
            print("OKay Thank U")
            break
        if not question:
            continue

        result=ask_question(question)

        print("\n" + "="*60)
        print(f'Answer:\n{result['answer']}')
        print("\nSources:")

        for doc in result['sources']:
            page=doc.metadata.get("page")
            snippet=doc.page_content[:100].replace("\n"," ")
            print(page,snippet,"....")
        print("="*60+ "\n")

if __name__=="__main__":
    chat_loop()

