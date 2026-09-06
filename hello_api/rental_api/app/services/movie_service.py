
from app.repositories.movie_repository import create_movie,get_movies

from app.schemas.movie import MovieCreate

def add_movie(movie_data:MovieCreate):
    return create_movie(movie_data)

def get_all_movie():
    return get_movies()
