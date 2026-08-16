from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

class Item(BaseModel):
    name:str
    price:float
    is_offer:bool | None = None

class student(BaseModel):
    name:str
    age:int
    course:str

@app.get("/")
def read_root(name=str):
    return {"Hello":name }

@app.post("/student")
def student_info(student:student):
    return{student.name:"Avinash",student.age:24,student.course:"AI"}

@app.get("/students")
def student_info(student:student):
    return {"name":student.name,"age":student.age,"course":student.course}

@app.get("/items/{item_id}")
def read_items(item_id:int,item: Item):
    return {"items_name":item.name,"items_id":item_id}