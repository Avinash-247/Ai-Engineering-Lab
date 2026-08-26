from fastapi import FastAPI
from router import users,product,orders
app=FastAPI()


app.include_router(users.router)
app.include_router(product.router)
app.include_router(orders.router)
@app.get("/user")
def get_users():
    return {"message":"yes working"}