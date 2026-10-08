from claude_agent_sdk import (
    ClaudeAgentOptions,Message,
    SystemMessage,UserMessage,ResultMessage,
    AssistantMessage,ClaudeSDKClient)

from claude_agent_sdk.types import TextBlock
Model_Name='claude-haiku-4-5'

def base_options(**arguments)->ClaudeAgentOptions:
    settings={
        "model":Model_Name,
        "max_turns":3
    }

    settings.update(arguments)
    options=ClaudeAgentOptions(**settings)

def parse_message(message:Message):
    if isinstance(message,SystemMessage):
        print("subtype:{message.subtype}")

    elif isinstance(message,AssistantMessage):
        for block in message.content:
            if isinstance(block,TextBlock):
                print("text{block.text}")

    elif isinstance(message,ResultMessage):
        print(f"duration{message.duration_ms}ms")
        print(f"cost{message.total_cost_usd}")
        print(f"session_id:{message.session_id}")
