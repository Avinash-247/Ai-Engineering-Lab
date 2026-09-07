from pydantic import BaseModel

class MovieCreate(BaseModel):
    id:int
    title:str
    description: str
    genre: str
    director: str
    release_year: int
    rating: float
    language: str
    country: str
    duration: int
    location: str

class MovieResponse(BaseModel):
    id:int
    title:str
    description: str
    genre: str
    director: str
    release_year: int
    rating: float
    language: str
    country: str
    duration: int
    location: str

class MovieUpdate(BaseModel):
    title:str
    description: str
    genre: str
    director: str
    release_year: int
    rating: float
    language: str
    country: str
    duration: int
    location: str

