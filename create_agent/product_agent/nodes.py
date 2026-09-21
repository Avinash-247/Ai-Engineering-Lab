from state import AdvisorState
from langgraph.prebuilt import ToolNode,tools_condition
from utils import get_default_model
from tools import (
    get_all_products,
    get_product,
)

all_tools=[get_product,
               get_all_products]


def get_model_with_tools(tools):

    llm=get_default_model()
    return llm.bind_tools(tools=tools)
def assistant(state:AdvisorState):
    llm_with_tools=get_model_with_tools(
        tools=all_tools)

    return state

def get_tool_node()->ToolNode:
    """toolNodes"""
    return ToolNode(tools=all_tools)

def capture_customer_info():
    """tool"""
    pass