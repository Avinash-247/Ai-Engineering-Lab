import os 
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),

)

message=client.messages.create(
    max_tokens=30,
    messages=[
        {
            "role":"user",
            "content":"what is capital of india",
        }
    ],
    model="claude-haiku-4-5",
)


for block in message.content:
    if block.type=="text":
        print(block.text)