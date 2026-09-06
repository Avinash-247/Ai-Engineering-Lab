from app.database.session import SessionLocal
from app.models.movie import Movie

db = SessionLocal()

movies = db.query(Movie).all()

for movie in movies:
    print(movie.id, movie.title, movie.release_year)

db.close()