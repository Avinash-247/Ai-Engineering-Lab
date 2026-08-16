from fastapi import FastAPI

app=FastAPI()

@app.post("/user")
def create_user():
    return {"message":"user created"}

from pydantic import BaseModel

class User(BaseModel):
    name:str
    age:int

@app.post("/user")
def user_data(user:User):
    return {"name":user.name,"age":user.age}

@app.get("/user")
def user_data(user:User):
    return {"name":user.name,"age":user.age}


@app.get("/items/{item_id}")
def read_items(item_id:int,item: int):
    return {"items_name":item.name,"items_id":item_id}