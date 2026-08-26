from fastapi import APIRouter

router=APIRouter()

@router.get("/users")
def get_users():
    return {"user_list"}

@router.get("/users{user_id}")
def get_user_id(user_id:int):
    return {"user_id":user_id}
