from typing import Annotated
from claude_agent_sdk import tool,create_sdk_mcp_server,query,ResultMessage
from dotenv import load_dotenv

load_dotenv()

@tool(
        "get_topic",
        "get the current topic to search in the web",
        {
            "path": Annotated[str,"Topic File location"]
        },
)
def get_topic(path="./downloads/topic.txt")->str:
    with open(path,mode='r') as file:
        return file.readlines()[0]

topic_server=create_sdk_mcp_server(
    name="topic",
    version="1.0.0",
    tools=[get_topic],
)


async def main():
    options=create_sdk_mcp_server(
        mcp_servers={"topic":topic_server},
        allowed_tools=["mcp__topic__get_topic"],
        tools=["Read","Glob","PowerShell"]
    )

    async for messages in query(
        prompt="what is the topic",
        options=options,
    ):
        if isinstance(messages,ResultMessage)and messages.subtype=="success":
            print(messages.result)

        

if __name__=="__main__":
    print(get_topic())