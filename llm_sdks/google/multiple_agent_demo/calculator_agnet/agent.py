from google.adk.agents.llm_agent import Agent

def calculate(a:float|int,b:float|int,operator:str)->float|int:
    """perform addition, sub, multiple or division on two numbers."""

    if operator =="add":
        result=a+b
    elif operator =="subtact":
        result=a-b
    elif operator == "Multiply":
        result=a*b

    elif operator=="divide":
        if b ==0:
            return {"error": "we cannotdevide by zero"}
        result =a/b
    else:
        return {
            "error":"Invalid operator. use add, substract,multiply or divide."
        }
    return {
        "a":a,
        "b":b,
        "operator":operator,
        "result":result
    }
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='An agent that performs basic mathematical calculations.',
    instruction=(
        "You are a calculator assistant."
        "use the calculate tool for arithmetic calculations."
        "choose the correct operation based on the user's requesr."
        "explain the result clearly."
        "Never divide by zero"
    ),
    tools=[calculate],

)