from langgraph.graph import StateGraph,START,END,MessagesState
from create_agent10 import model
from langchain.tools import tool
from langgraph.prebuilt import ToolNode,tools_condition
from langchain.messages import AIMessage,SystemMessage,HumanMessage,ToolMessage


@tool
def get_skin_care(brand_name: str) -> str:
    """
    Provides a beginner-friendly description of a skin care brand.

    Args:
        brand_name (str): The name of the skin care brand.

    Returns:   
        str: A formatted message introducing the brand.
    """
    return f"hello sir/madam {brand_name}, this is the skin care brand also best for beginners."


@tool
def get_hair_care(brand_name: str) -> str:
    """
    Provides a beginner-friendly description of a hair care brand.

    Args:
        brand_name (str): The name of the hair care brand.

    Returns:
        str: A formatted message introducing the brand.
    """
    return f"hello sir/madam {brand_name}, this is the hair care brand also best for beginners."


@tool
def get_body_care(brand_name: str) -> str:
    """
    Provides a beginner-friendly description of a body care brand.

    Args:
        brand_name (str): The name of the body care brand.

    Returns:
        str: A formatted message introducing the brand.
    """
    return f"hello sir/madam {brand_name}, this is the body care brand also best for beginners."


llm=model
tools=[get_skin_care,get_hair_care,get_body_care]
llm_with_tool=llm.bind_tools(tools=tools)
def chat(state:MessagesState)->MessagesState:
    # state['messages']=[llm_with_tool.invoke(state['messages'])]
    response=llm_with_tool.invoke(state["messages"])
    return {"messages":[response]}


tools_node=ToolNode(tools=tools)
graph_state=StateGraph(MessagesState)

graph_state.add_node("chat",chat)
graph_state.add_node("tools",tools_node)


graph_state.set_entry_point("chat")

graph_state.add_conditional_edges(
    "chat",
    tools_condition)

graph_state.add_edge("tools","chat")

graph=graph_state.compile()

result=graph.invoke({
    "messages":[
        SystemMessage("if the user can ask irrlevent from the question, and just return the what the answer get whtn tool get called., dont write extra content"),
        HumanMessage("i want to start a skin care rotine brand like saska is it good to use")
    ]
})

print(result)