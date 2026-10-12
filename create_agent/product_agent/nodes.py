from state import AdvisorState
from langgraph.prebuilt import ToolNode,tools_condition
from utils import get_default_model
from tools import (
    get_all_products,
    get_product,
)
from langchain_core.messages import SystemMessage,BaseMessage,HumanMessage,RemoveMessage
from prompts import SYSTEM_PROMPT

summery_trigger=12
keep_recent=6

all_tools=[get_product,get_all_products]


def get_model_with_tools(tools):

    llm=get_default_model()
    return llm.bind_tools(tools=tools)



def assistant(state:AdvisorState):
    llm_with_tools=get_model_with_tools(
        tools=all_tools
    )
    replay =llm_with_tools.invoke([SystemMessage(SYSTEM_PROMPT)]+state['messages'])
    state['messages']=[replay]

    return state           #{'message',[replay]}

def safe_cut(messages:list[BaseMessage],keep_recent:int)->int:
    cut=len(messages) -keep_recent
    while cut>0 and not isinstance(messages[cut],HumanMessage):
        cut-=1
    return cut

def summerize_conversaion(state:AdvisorState):
    messages=state["messages"]
    cut=safe_cut(messages,keep_recent)
    old=messages[:cut]
    instruction=(
        "summerize this part of product-advice conversation in under 120 words."
        "keep the customers state concerns and which product were discussed."
        "do not invent anything"
    )
    previous=state.get("summery")
    if previous:
        f"summery so dar {previous}\n\n{instruction} Extended it"
    summery=get_default_model().invoke([SystemMessage(instruction)]).content()

    return {
        "summary":summery,
        "messages":[RemoveMessage(id=m.id) for m in old]
    }




def get_tool_node()->ToolNode:
    """toolNodes"""
    return ToolNode(tools=all_tools)

def capture_customer_info(state:AdvisorState):
    return state






