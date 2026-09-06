from sqlalchemy import Column, Integer, String,Float
from app.database.connection import Base

class Movie(Base):
    __tablename__ ="movies"

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    description=Column(String)
    genre=Column(String)
    director=Column(String)
    release_year=Column(String)
    rating=Column(Float)
    language=Column(String)
    country=Column(String)
    duration=Column(Integer)
    location=Column(String)



