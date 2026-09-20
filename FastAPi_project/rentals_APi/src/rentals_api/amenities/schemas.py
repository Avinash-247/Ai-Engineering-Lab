from pydantic import BaseModel

class AmenityCreate(BaseModel):
    name: str

class AmenityRead(BaseModel):
    id:int
    name:str
    