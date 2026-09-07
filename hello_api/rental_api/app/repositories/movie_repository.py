from app.database.session import SessionLocal

from app.models.movie import Movie

from app.schemas.movie import (
    MovieCreate,MovieResponse,
    MovieUpdate)

def create_movie(movie_data:MovieCreate):
    print("Repository: getting movie from DB")

    db=SessionLocal()

    try:
        movie=Movie(
            title=movie_data.title,
            description=movie_data.description,
            genre=movie_data.genre,
            rating=movie_data.rating,
            country=movie_data.country,
            director=movie_data.director,
            release_year=movie_data.release_year,
            language=movie_data.language,
            duration=movie_data.duration,
            location=movie_data.location

        )

        db.add(movie)
        db.commit()
        db.refresh(movie)

        return movie

    finally:
        db.close()


def get_movies():
    db=SessionLocal()

    try:
        movies=db.query(Movie).all()
        return movies

    finally:
        db.close()

def movie_by_id(movie_id:int):
    db=SessionLocal()

    try:
        movie=db.query(Movie).filter(Movie.id==movie_id).first()
        return movie
    finally:
        db.close()

def update_movie_by_id(movie_id:int,movie_data:MovieUpdate):
    db=SessionLocal()

    try:

        movie=db.query(Movie).filter(Movie.id==movie_id).first()

        if movie:
            movie.title = movie_data.title
            movie.description = movie_data.description
            movie.genre = movie_data.genre
            movie.rating = movie_data.rating
            movie.country = movie_data.country
            movie.director = movie_data.director
            movie.release_year = movie_data.release_year
            movie.language = movie_data.language
            movie.duration = movie_data.duration
            movie.location = movie_data.location

            db.commit()
            db.refresh(movie)

        return movie
    finally:
        db.close()


def delete_movie_by_id(movie_id:int):
    db=SessionLocal()
    try:
        movie =db.query(Movie).filter(Movie.id==movie_id).first()

        if movie:
            db.delete(movie)
            db.commit()
        return movie
    finally:
        db.close()

        