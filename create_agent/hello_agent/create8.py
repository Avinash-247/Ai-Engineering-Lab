from langgraph.graph import START,END,StateGraph
from typing import TypedDict,Literal


class operations(TypedDict, total=False):
    a:int|float
    b:int|float
    options:Literal["add","sub"]
    result:int|float

def decision(state:operations)->Literal["add","sub"]:
    if state["options"]=="add":
        return "add"
    return "sub"
def add(state:operations):
    return{
        "result": state["a"]+state["b"]
    }
def sub(state:operations):
    return{
        "result":state["a"] - state["b"]
    }

graph_state=StateGraph(operations)

graph_state.add_node("add",add)
graph_state.add_node("sub",sub)
graph_state.set_finish_point("add")
graph_state.set_finish_point("sub")

graph_state.add_conditional_edges(
    START,
    decision)

graph=graph_state.compile()

if __name__=="__main__":
    result=graph.invoke(operations(a=20,b=30,options="sub"))
    print(result)