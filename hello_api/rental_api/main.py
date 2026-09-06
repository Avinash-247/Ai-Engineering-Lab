"""from  test import hello
print("this is th etasj and its complete")
print(hello.message)"""

from app.routers.movies import router
from fastapi import FastAPI

app=FastAPI()

app.include_router(router)


