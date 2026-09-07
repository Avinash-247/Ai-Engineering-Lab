
from app.repositories.movie_repository import (
    create_movie,
    get_movies,
    movie_by_id,
    update_movie_by_id,
    delete_movie_by_id)

from app.schemas.movie import MovieCreate,MovieResponse,MovieUpdate

#this is for post movie
def add_movie(movie_data:MovieCreate):
    return create_movie(movie_data)

def get_all_movie():
    return get_movies()

def get_movie(movie_id:int):
    return movie_by_id(movie_id)

def update_movie(movie_id:int,movie_data:MovieUpdate):
    return update_movie_by_id(movie_id,movie_data)

def delete_movie(movie_id:int):
    return delete_movie_by_id(movie_id)
