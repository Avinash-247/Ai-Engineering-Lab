from fastapi import FastAPI,Query
from pydantic import BaseModel

app=FastAPI()

class Student(BaseModel):
    name:str
    age:int
    course:str

@app.post("/student")
def create_student(student:Student):
    return {
        "name":student.name,
        "age":student.age,
        "course":student.course
    }

@app.get("/student")
def get_students():
    return {
        "name":"Avinash",
        "age":35,
        "course":"AI"
    }
@app.get("/student{details}")

def create_details(name:str,
                   age:int= Query(ge=18,le=70)):
    return {"name":name, "age":age}