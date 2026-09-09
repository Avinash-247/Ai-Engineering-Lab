from langgraph.graph import StateGraph
from langgraph.graph import START,END

from typing import TypedDict

class OperationState(TypedDict):
    a:int|float
    b:int|float
    sum:None|int
    product:None|int
    diff:None|int

def add(state:OperationState)->OperationState:
    state['sum']=state['a']-state['b']
    return state
def sub(state:OperationState)->OperationState:
    state['product']=state['a']*state['b']
    return state

def mul(state:OperationState)->OperationState:
    state['diff']=state['a'] - state['b']
    return state

state_graph=StateGraph(OperationState)
state_graph.add_node("add",add)
state_graph.add_node("sub",sub)
state_graph.add_node("mul",mul)

state_graph.add_edge(START,"add")
state_graph.add_edge("add","sub")
state_graph.add_edge("sub","mul")
state_graph.add_edge("mul",END)

graph=state_graph.compile()

if __name__=="__main__":
    result=graph.invoke(OperationState(a=5,b=9))
    print(result)
