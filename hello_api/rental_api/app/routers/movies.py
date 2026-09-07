from fastapi import APIRouter
from app.services.movie_service import (
    add_movie,get_all_movie,
    get_movie,update_movie,
    delete_movie)
from app.schemas.movie import (
    MovieResponse,MovieUpdate,
    MovieCreate)
router=APIRouter(
    tags=["movies"]
)
"""
@router.get("/{movie_id}")
def create_movie(movie_id:int):
    return add_movie(movie_id)

@router.get("/{movie_id}")
def get_movie_by_id(movie_id:int):
    return add_movie(movie_id)


@router.get("/")
def get_all_movies():
    return get_all_movie()

@router.get("/",response_model=list[MovieResponse])
def get_f1():
    return get_all_movie"""



@router.get("/{getting_movie_by__id}",response_model=MovieResponse)
def movie_by(movie_id:int):
    return get_movie(movie_id)

@router.put("/{updating_by_movie_id}",response_model=MovieResponse)
def update_movie_by_info(movie_id:int,movie_data:MovieUpdate):
    return update_movie(movie_id,movie_data)

#post or for adding new movie
@router.post("/{adding_new_movie}",response_model=MovieResponse)
def create_movie(movie_data:MovieCreate):
    return add_movie(movie_data)

#deleting function
@router.delete("/{delete_movie}",response_model=MovieResponse)
def deleting_movie(movie_id:int):
    return delete_movie(movie_id)