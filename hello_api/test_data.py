from database import users
from fastapi import FastAPI,HTTPException
app=FastAPI()
@app.get("/users")
def get_users():
    return users

@app.get("/users/{first_name}")
def get_user(user_id: int):
    for user in users:
        if user["id"]== user_id:
            return user

    raise HTTPException(
        status_code=404,
        details="user not found"
    )