from pydantic import BaseModel,Field,EmailStr
from fastapi import FastAPI
from typing import Annotated
app=FastAPI()
class user(BaseModel):
    first_name: str =Field(min_legth=2,max_length=50)
    last_name:str= Field(min_length=2,max_length=50)

    age:int = Field(ge=18,le=60)

    email:EmailStr

    phone_number:str = Field(
        pattern=r"^\+?[0-9]{10,15}$"
    )

    adhar_number:str = Field(
        pattern=r"^[0-9]{10,15}$"
    )

    credit_card_number : str = Field(
        pattern=r"^[0-9]{16}"
    )



@app.post("/users")
def create_user(user:user):
    return { 
        "first_name":user.first_name,
        "last_name": user.last_name,
        "age":user.age,
        "email":user.email,
        "adhar_number":user.adhar_number,
        "credit_card":user.credit_card_number,
        "ph.NO":user.phone_number,
    }

