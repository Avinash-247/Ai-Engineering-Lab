from mcp import Client,StdioServerParameters
import asyncio
from typing import Any
tool_dict:dict[str,Any]={}
async def main()->None:
    async with Client("http://localhost:8000/mcp") as client:
        result= await client.list_tools()
        for tool in result.tools:
            #print(f"tool_name {tool.name}")
            #print(f"input_schema  {tool.input_schema}")

            tool_dict[tool.name]=tool.input_schema
        while True:
            
            for name in tool_dict:
                print(f"name: {name}")
            choice =input("Enter the tool name: ")
            if choice in tool_dict:
                a=int(input("enter the value of A:  "))
                b=int(input("ENter the value of B: "))

                tool_call_result=await client.call_tool(choice, {'a':a,'b':b})
                print(tool_call_result)
                print(f"result= {tool_call_result.structured_content['result']}")



            choice=input("Enter n to quit else to continue : ")
            if choice.strip().lower() =="n":
                break


    

if __name__=="__main__":
    asyncio.run(main())