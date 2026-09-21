from typing import TypedDict,Annotated,Optional

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages


class AdvisorState(TypedDict,total=False):
    messages:Annotated[list[BaseMessage],add_messages]
    product_id:Optional[str]
    mobile_number:Optional[str]
    email:Optional[str]
    customer_name:Optional[str]
    lead_status:Optional[str]

        