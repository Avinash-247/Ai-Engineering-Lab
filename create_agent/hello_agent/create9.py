from typing import TypedDict,Literal

from langgraph.graph import START,StateGraph,END

class Operations(TypedDict,total=False):
    a:int
    b:int
    count:int
    result:int
def add(state:Operations)->Operations:
        state["result"]= state["a"]+ state["b"]
        state["count"]+=1
        return state 

def decision(state:Operations)->Literal["pending","completed"]:
    if state["count"]<3:
        return "pending"
    return "completed"

graph_state=StateGraph(Operations)
graph_state.add_node("add",add)
graph_state.add_edge(START,"add")
graph_state.add_conditional_edges(
    "add",
    decision,
    {
        "pending":"add",
        "completed":END
    }
)

graph=graph_state.compile()
