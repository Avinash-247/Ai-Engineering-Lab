from app.database.session import SessionLocal

from app.models.movie import Movie

from app.schemas.movie import MovieCreate

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
        