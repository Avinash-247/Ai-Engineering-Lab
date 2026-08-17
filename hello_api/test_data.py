from database import users
from fastapi import FastAPI,HTTPException,Path
from typing import Annotated,Literal
app=FastAPI()
# @app.get("/users")
# def get_users():
#     return users

# @app.get("/users/{first_name}")
# def get_user(user_id: int):
#     for user in users:
#         if user["id"]== user_id:
#             return user

#     raise HTTPException(
#         status_code=404,
#         details="user not found"
#     )

@app.get("/users/{info}")
def create_cat(category:str,price:int,brand:str):
    return{"category":category,"price":price,"brand":brand}

@app.get("/products/{product_id}")
def product_datails(product_id: int ,category:str,price:int,brand:str , model:int):
    return{
        "product_id":product_id,
        "category":category,
        "price":price,
        "brand":brand,
        "model":model
    }

@app.get("/employe")
def enter_details(severity: Annotated[int, Path(ge=1, le=50)]):
    return {"senioraty":severity}

@app.get("/seurity")
def enter(security: Literal["low","Mid","High","extreme"]):
    return {"secure":security}