from langchain.tools import tool
from langgraph.graph import StateGraph,START,END,MessagesState
from typing import TypedDict
from langchain.chat_models  import init_chat_model,BaseChatModel
from dotenv import  load_dotenv
from langchain.messages import HumanMessage,AIMessage,SystemMessage
from langgraph.prebuilt import ToolNode,tools_condition

load_dotenv()

@tool
def get_wether(city:str)->str:
    """this  functions is ment by based on the city its gives a wether report"""
    return f"Here the {city}wether is so sunny to day"

@tool
def get_currency(country:str)->str:
    """this function is called when the user wants particular {country currency}"""
    return f"{country}currency is (RS rupees) okay"

tools=[get_currency,get_wether]

llm='google_genai:gemini-3.5-flash-lite'
model=init_chat_model(model=llm)

llm_with_tool=model.bind_tools(tools=tools)

def chat(state: MessagesState)->MessagesState:
    state["messages"]=llm_with_tool.invoke(state['messages'])
    return state

tool_node=ToolNode(tools=tools)

graph_state=StateGraph(MessagesState)

graph_state.add_node("chat",chat)
graph_state.add_node("tools",tool_node)

graph_state.set_entry_point("chat")
graph_state.add_conditional_edges(
    "chat",
    tools_condition
)

graph_state.add_edge("tools","chat")
#graph_state.add_edge("chat",END)

graph=graph_state.compile()

result=graph.invoke({
    "messages":[
        SystemMessage("""Act as a judge. 
                - If no tool is relevant to the human message, respond with: 'Sorry, I don’t have enough sources to answer this question.'
                - If the answer is wrong but a relevant tool is available, simply return the tool output. 
                 - Do not verify whether the tool’s answer is right or wrong."""
                ),

        HumanMessage("what is the currency of india &how the wether in india right now")
    ]
})

print(result)