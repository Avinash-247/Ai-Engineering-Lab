from typing import Optional

def say_hello(name: Optional[str]=None)->str:
    """Provides a simple greeting. If a name is provided, it will be used.

    Args:
        name (str, optional): The name of the person to greet. Defaults to a generic greeting if not provided.

    Returns:
        str: A friendly greeting message.
    """
    if name:
        greeting=f"Hello,{name}"
    else:
        greeting="Hello there"

    return greeting
def say_goodbye()->str:
    return "GoodBye Have a great day"

print("Greeting and Fare well tools defined")


print(say_hello("avi"))

