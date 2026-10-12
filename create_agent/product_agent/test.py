from main import graph

from state import AdvisorState
from langchain_core.messages import HumanMessage
result=graph.invoke(AdvisorState(
    messages=[
        HumanMessage("I need a fix for skin detan")

    ]
))

print(result)