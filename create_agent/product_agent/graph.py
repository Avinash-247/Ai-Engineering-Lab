from langgraph.graph import START,StateGraph,END
from state import AdvisorState
from langgraph.prebuilt import tools_condition
from nodes import (
    assistant,get_all_products,
    get_tool_node,capture_customer_info
)
def create_graph()->StateGraph:
    """this method create a graph

    """
    State_graph=StateGraph(AdvisorState)
    State_graph.add_node("assistant",assistant)
    State_graph.add_node("tools",get_tool_node)
    State_graph.add_node("capture",capture_customer_info)



    State_graph.add_edge(START,"assistant")
    State_graph.add_conditional_edges(
        "assistant",
        tools_condition
              )

    State_graph.add_edge("assistant","capture")
    State_graph.add_edge("capture",END)
    return State_graph



