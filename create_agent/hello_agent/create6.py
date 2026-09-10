from typing  import TypedDict
from langgraph.graph  import StateGraph,START,END
class Store(TypedDict):
    shirt:int|float
    pant:int|float
    t_shirt:int|None
    cost_shirt:int|float
    discout_on_cost:int|float

def cost_shirt(state:Store)->Store:
    state["cost_shirt"] = state["pant"] + state["shirt"]
    return  state
def discout_on_cost(state:Store)->Store:
    state["discout_on_cost"]=state["pant"]+state["shirt"]
    if state["discout_on_cost"]>=1500:
        state["discout_on_cost"]=state["discout_on_cost"]-500
    return state

state_graph=StateGraph(Store)

state_graph.add_node("total_cost",cost_shirt)
state_graph.add_node("discount",discout_on_cost)

state_graph.add_edge(START,"total_cost")            
state_graph.add_edge("total_cost","discount")
state_graph.add_edge("discount",END)

graph=state_graph.compile()

if __name__=="__main__":
    result=graph.invoke({"shirt":600,"pant":600})
    print(result)