from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

'''class Item(BaseModel):
    name:str
    price:float
    is_offer:bool | None = None'''

@app.get("/")
def read_root(name=str):
    return {"Hello":name }


@app.get("/items/{item_id}")
def read_items(item_id:int,item: Item):
    return {"items_name":item.name,"items_id":item_id}