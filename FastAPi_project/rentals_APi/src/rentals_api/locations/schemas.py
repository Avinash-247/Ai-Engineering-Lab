from pydantic import BaseModel

class LocationCreate(BaseModel):
    city: str
    locality:str
    state:str
    description:str |None

class LocationRead(BaseModel):
    id:int
    city:str
    locality:str
    state:str
    description:str |None = None

    