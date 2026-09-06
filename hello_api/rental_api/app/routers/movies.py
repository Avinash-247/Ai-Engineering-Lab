from fastapi import APIRouter
from app.services.movie_service import add_movie,get_all_movie
router=APIRouter()

@router.get("/movies/{movie_id}")
def create_movie(movie_id:int):
    return add_movie(movie_id)

@router.get("/movies/{movie_id}")
def get_movie_by_id(movie_id:int):
    return add_movie(movie_id)


@router.get("/movies")
def get_movies():
    return get_all_movie()

