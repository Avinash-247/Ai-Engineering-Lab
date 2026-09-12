from typing import TypedDict
from langgraph.graph import START,END,StateGraph

from typing import Annotated
import operator
class operations(TypedDict):
    a:int|float
    b:int|float
    result:Annotated[list[int],operator.add]



def add(state:operations)->operations:
    # state["result"]=state["a"]+state["b"]
    # return state
    return {
        "result": [state['a'] + state['b']]
    }

def sub(state:operations)->operations:
    # state["result"]=state["a"]-state["b"]
    # return state
    return {
        "result": [state['a'] - state['b']]
    }
state_graph=StateGraph(operations)    

state_graph.add_node("add",add)
state_graph.add_node("sub",sub)

state_graph.add_edge(START,"add")
state_graph.add_edge("add",END)
state_graph.add_edge(START,"sub")
state_graph.add_edge("sub",END)

graph=state_graph.compile()


if __name__=="__main__":

    result=graph.invoke(operations(a=20,b=12))

    print(result)
