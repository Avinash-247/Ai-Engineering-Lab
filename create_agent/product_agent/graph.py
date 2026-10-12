from langgraph.graph import START,StateGraph,END
from state import AdvisorState
from langgraph.prebuilt import tools_condition
from nodes import (
    assistant,get_all_products,
    get_tool_node,capture_customer_info,
    all_tools,summerize_conversaion,
    summery_trigger,
)


def route_exit(state:AdvisorState)->str:
    if len(state("messages")) >summery_trigger:
        return "summerize"
    return END

def router_After_assistant(state:AdvisorState)->str:
    last=state["messages"][-1]
    if getattr(last,"tool_calls",None):
        return "tools"    
    return route_exit(state)

def create_graph()->StateGraph:
    """this method create a graph

    """
    State_graph=StateGraph(AdvisorState)
    State_graph.add_node("assistant",assistant)
    State_graph.add_node("tools",get_tool_node())
    #State_graph.add_node("capture",capture_customer_info)
    State_graph.add_node("summerize",summerize_conversaion)




    State_graph.add_edge(START,"assistant")
    State_graph.add_conditional_edges(
        "assistant",
        tools_condition,
        {
            "tools":"tools",
            "summerize":"summerize",
            END:END,

        }
    )
    State_graph.add_edge("tools","assistant")
    #State_graph.add_edge("assistant","capture")
    State_graph.add_edge("capture",END)
    return State_graph



