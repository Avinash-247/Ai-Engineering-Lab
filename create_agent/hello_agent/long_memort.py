from dotenv import load_dotenv
import os
load_dotenv()

model_name='google_geniai:gemini-3.5-flash-lite'

from langchain.agents import create_agent

from langchain.tools import tool
@tool()
def add(a:int|float,b:int|float) -> int|float :
    """Adds two numbers
    Args:
        a(int|float)
        b(int|float)
    return:
        int|float:sum of two numbers
    """
    return a+b

@tool
def sub(a:int|float,b:int):
    return a-b
