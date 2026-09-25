from langgraph.graph import MessagesState,StateGraph,START,END
from langchain.tools import tool
from langgraph.prebuilt import ToolNode,tools_condition
from langchain.messages import HumanMessage,AIMessage,SystemMessage,ToolMessage

from cafe_menu import MENU
from llm_model import get_model


@tool
def get_menu() -> str:
    """Get the cafe menu with prices."""
    return "\n".join(
        f"{item.title()} - {price}"
        for item,price in MENU.items()
    )

@tool
def check_items_availability(item: str) -> str:
    """Check whether a cafe item is available."""

    if item.lower() in MENU:
        return f"{item} is available."

    return f"Sorry, {item} is not available."

@tool
def calculate_bill(items:str,quality:int)->str:
    """calculating bill """
    price =MENU.get(items)
    if price is None:
        return f"{items} is not available"
    
    total=price*quality
    return f"{quality} {items} = {total}"


@tool
def price_order(items:str)->str:
    "calculating the total price of multiple cafe items."
    total=0

    for item, quantily in items.items():
        price=MENU.get(items)

        if price is None:
            return f"{items} is not available"
        total+= price*quantily
    return f"total order price:{total}"

tools=[get_menu,check_items_availability,calculate_bill,price_order]

tool_node=ToolNode(tools=tools)
llm=get_model()

llm_with_tools=llm.bind_tools(tools=tools)

def chat(state:MessagesState):
    response=llm_with_tools.invoke(state["messages"])
    return {"messages":[response]}

state_graph=StateGraph(MessagesState)

state_graph.add_node("chat",chat)
state_graph.add_node("tools",tool_node)

state_graph.set_entry_point("chat")
state_graph.add_conditional_edges(
    "chat",
    tools_condition
    )

state_graph.add_edge("tools","chat")
# state_graph.add_edge("chat",END)

graph=state_graph.compile()

result=graph.invoke(
    {
        "messages":[
            SystemMessage(
                content="""
                You are CafeMate, a cafe ordering assistant.

                When a customer orders an item:
                - If quantity is not mentioned, assume quantity = 1.
                - Check whether the item is available.
                - Calculate the price for the requested quantity.
                - If multiple items are ordered, calculate the total order price.
                """
            ),
            HumanMessage(content="i want a cappuccino")
        ]
    }
)

print(result[-1])

