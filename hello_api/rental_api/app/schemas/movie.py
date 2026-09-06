from pydantic import BaseModel

class MovieCreate(BaseModel):
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