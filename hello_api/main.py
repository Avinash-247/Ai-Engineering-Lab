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