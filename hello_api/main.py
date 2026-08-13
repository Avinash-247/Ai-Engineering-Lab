'''from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "FastAPI is working!"}


@app.get("/hello")
def hello():
    return {"message": "Hello Avinash!"}

@app.get("/items{item_id}")
def read_item(item_id:int,q:str|None=None):
    return {"itam_id":item_id, "q":q}'''


from fastapi import FastAPI

app=FastAPI()

@app.get("/")
def home():
    return {"message":"working its goodto start"}

@app.get("/users/{user_id}")

def  user_data(user_id:int,message:str):
    return {"user_id":user_id,"message":message}

#update version
@app.get("/users/{user_id}")
def user_data(user_id:int):
    return {"user_is":user_id,"message":"user Found"}

@app.get("users{user_id}")
def data(user_id:int,message:str,name:str):
    return {"user_id":user_id,"message":message,"name":name}

@app.get("/products/{products_id}")
def product(product_id:int,search:str | None=None):
    return {"product_id":product_id,"search":search}

