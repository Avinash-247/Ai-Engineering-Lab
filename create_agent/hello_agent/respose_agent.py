from langchain.chat_models import init_chat_model
from langchain_core.messages import (HumanMessage,
                                     AIMessage,SystemMessage)
from dotenv import load_dotenv


load_dotenv()

model=init_chat_model(model="gemini-3.5-flash-lite",
                      model_provider="google_genai")

message=[
        HumanMessage("this is Avi"),
        HumanMessage("what is capital of india"),
        HumanMessage("what is My name")
    ]


responses=model.invoke(message)
# responses.pretty_print()
for response in responses:
    print(response)



'''llm=ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

ins1=llm.invoke("Hi this is Avinash")
print(ins1)
message=(("what is my name"),ins1)
ins2=llm.invoke(message)
print(ins2)'''



