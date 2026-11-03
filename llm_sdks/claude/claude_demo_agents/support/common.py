"""
common.py - common utils class

"""
from typing import Any,Callable

from claude_agent_sdk import (
    ClaudeSDKClient,ClaudeAgentOptions,
    create_sdk_mcp_server,AssistantMessage,ResultMessage,
    TextBlock,ToolUseBlock,
)

ORDERS={
    "cust_101":{"Qb-5521":{"status":"out of delivery","eta":"8:40 Pm", "items":"2*veg biryani"}},
    "cust_202":{"qb-7710":{"status":"delivered","eta":None,"items":"1*Haleem"}}

}

ENV={"CLAUDE_CODE_DISALE_AUTO_MEMORY":"1"}




