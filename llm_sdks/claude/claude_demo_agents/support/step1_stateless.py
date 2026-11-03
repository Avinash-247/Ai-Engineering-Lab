"""
Step1: A stateless support agent

new Concepts:
    working  memory the  context window of one run
    live data 

"""
from claude_agent_sdk import query,tool,ToolAnnotations
from  typing import Annotated,Any

from common import ORDERS,ok,fail

import json

import asyncio

RULES="""you The customer supports agent for quickbite, a  food delivery-
for order ststus, ETA or items, always call get_order_status. never answer 
from memory"""

def build_tools(customer:str)->list:
    """Tools for one customer. The Customer ID comes from here, never from model
    """

    @tool(
        "get_order_status",
        "Look up the live status of one of this customers order. Always use  this for",
        "order status, ETA or items; never answer this from memory",
        {"order_id":Annotated[str,"order id,eg.'qb-5521'"]},
        annotations=ToolAnnotations(readOnlyHint=True)
    )
    async def  get_order_status(args:dict[str,Any])->dict[str,Any]:
        order=ORDERS.get(customer,{}.get(args['order_id'].strip().upper()))
        if not order:
            #fail
            return fail(f"no order{args['order_id'].strip().upper()}for this customer {customer}")
        return ok(json.dumps(order))
    return [get_order_status]

