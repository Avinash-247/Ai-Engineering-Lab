"""
Step1: A stateless support agent

new Concepts:
    working  memory the  context window of one run
    live data 

"""
from claude_agent_sdk import query,tool,ToolAnnotations
from  typing import Annotated,Any

from common import ORDERS,ok,fail,print_message,make_options

import json

import asyncio
from dotenv  import  load_dotenv



RULES="""you The customer supports agent for quickbite, a  food delivery-
for order ststus, ETA or items, always call get_order_status. never answer 
from memory"""

def build_tools(customer:str)->list:
    """Tools for one customer. The Customer ID comes from here, never from model
    """

    # @tool(
    #     "get_order_status",
    #     "Look up the live status of one of this customers order. Always use  this for",
    #     "order status, ETA or items; never answer this from memory",
    #     {"order_id":Annotated[str,"Order_id,e.g.'Qb-5521'"]},
    #     annotations=ToolAnnotations(readOnlyHint=True)
    # )
    @tool(
            "get_order_status",
            "Look up the live status of one of this customer's orders. "
            "Always use this for order status, ETA or items; never answer from memory.",
            {"order_id": Annotated[str, "Order ID, e.g. 'QB-5521'"]},
            annotations=ToolAnnotations(readOnlyHint=True)
    )
    async def  get_order_status(args:dict[str,Any])->dict[str,Any]:
        order=ORDERS.get(customer,{}).get(args['order_id'].strip().upper())
        if not order:
            #fail
            return fail(f"no order{args['order_id'].strip().upper()}for this customer {customer}")
        return ok(json.dumps(order))
    return [get_order_status]


async def  ask_once(customer:str,text:str):
    """
    A bread new session for every quesion
    """
    try:
        async for message in query(
                prompt=text,
                options=make_options(RULES,build_tools(customer))):
            print_message(message)
        

    except Exception as error:
        print(f"(run ended:{error})")

async def chat(customer:str)->None:
    """A brand new session for every question"""
    print(f"stateless chat for {customer}. Every  quesion  starts from  nothing,Type  quit  to  stop\n")
    while  True:
        text=input("customer: ").strip()
        if text.lower() in {"quit","exit"}:
            break
        if text:
            await ask_once(customer,text)

# async def self_test()->None:
#     tools={t.name for t in build_tools("cust_101")}
#     print("live data: looking up never stored")


if __name__=="__main__":
    load_dotenv()

    asyncio.run(chat(customer="cust_101"))

