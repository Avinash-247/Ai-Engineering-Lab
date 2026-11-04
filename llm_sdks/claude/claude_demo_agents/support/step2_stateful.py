"""
Step 2: A stateful support agent

New concepts:
    short-term memory   the SDK session IS the conversation; resume=<session_id> continues it
    thread mapping      our code remembers which session belongs to which customer
    session store       the SDK also mirrors every transcript into SQLite, so a resume
                        still works on another machine or after the local files are gone
"""

from claude_agent_sdk import query,tool,ToolAnnotations
from  typing import Annotated,Any

from common import ORDERS,ok,fail,print_message,make_options

import json
import sqlite3

import asyncio
from dotenv  import  load_dotenv

from pathlib  import  Path

from session_stateful import SqliteSessionStore

DATA_DIR=Path(__file__).parent /"downloads"
DATA_DIR.mkdir(exist_ok=True)

SESSION_STORE=SqliteSessionStore(DATA_DIR/"session.db")



class Threads:
    """customer -> session_id. The SessionStore keeps transcripts; it doesn't know customers."""

    def __init__(self, path: Path):
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS threads (customer_id TEXT PRIMARY KEY, session_id TEXT NOT NULL)")

    def get(self, customer: str) -> str | None:
        row = self.db.execute("SELECT session_id FROM threads WHERE customer_id=?", (customer,)).fetchone()
        return row[0] if row else None

    def save(self, customer: str, session_id: str) -> None:
        with self.db:
            self.db.execute("INSERT OR REPLACE INTO threads VALUES (?, ?)", (customer, session_id))

    def end(self, customer: str) -> None:
        with self.db:
            self.db.execute("DELETE FROM threads WHERE customer_id=?", (customer,))


THREADS = Threads(DATA_DIR / "threads.db")

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
                options=make_options(
                    RULES,
                    build_tools(customer),  
                    session_store=SESSION_STORE,
                ),
            ):
            print_message(message)
        

    except Exception as error:
        print(f"(run ended:{error})")

async def chat(customer:str, new_thread:bool)->None:
    #"""A brand new session for every question"""
    if new_thread:
        THREADS.end(customer)
    state="continuing" if THREADS.get(customer) else "starting"
    print(f"{state} the thread for {customer}. Type 'quit' to stop.\n")
    #print(f"stateless chat for {customer}. Every  quesion  starts from  nothing,Type  quit  to  stop\n")
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

