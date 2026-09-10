from langgraph.graph.state import StateGraph,START,END
from typing import TypedDict,NotRequired,Required

class operation(TypedDict, total=False):
    a:int|float
    b:int|float
    result:NotRequired[int |float]

def add(operation:operation)->operation:
    """adding teo numbers
    Args:
         a:int|float
         b:int|float
        return a+b
    """
    return {
        "result":operation["a"]+operation["b"]}

def sub(operation:operation)->operation:
    """sub two numbers
    Args:
        a:int|float
        b:int|float
        return a-b
    """
    return {"result":operation["a"]-operation["b"]}

def mul(operation:operation)->operation:
    """MULL two numbers
        Args:
            a:int|float
            b:int|float
            return a*b
    """

    return {"result":operation["a"]* operation["b"]}
state_graph=StateGraph(operation)

state_graph.add_node("add",add)
state_graph.add_node("sub",sub)
state_graph.add_node("mul",mul)

state_graph.add_edge(START,"add")
state_graph.add_edge("add","sub")
state_graph.add_edge("sub",END)

state_graph.add_edge(START,"mul")
state_graph.add_edge("mul",END)

graph=state_graph.compile()

if __name__=="__main__":
    result=graph.invoke({"a":5,"b":6})
    print(result)
