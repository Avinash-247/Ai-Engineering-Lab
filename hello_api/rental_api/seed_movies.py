from app.database.session import SessionLocal
from app.models.movie import Movie


movies = [
    Movie(
        title="Inception",
        description="A thief who enters people's dreams.",
        genre="Sci-Fi",
        director="Christopher Nolan",
        release_year=2010,
        rating=8.8,
        language="English",
        country="USA",
        duration=148,
        location="Los Angeles"
    ),
    Movie(
        title="Interstellar",
        description="Explorers travel through a wormhole in space.",
        genre="Sci-Fi",
        director="Christopher Nolan",
        release_year=2014,
        rating=8.7,
        language="English",
        country="USA",
        duration=169,
        location="Iceland"
    ),
    Movie(
        title="The Dark Knight",
        description="Batman faces a dangerous criminal mastermind.",
        genre="Action",
        director="Christopher Nolan",
        release_year=2008,
        rating=9.0,
        language="English",
        country="USA",
        duration=152,
        location="Chicago"
    ),
    Movie(
        title="Avatar",
        description="A marine discovers the world of Pandora.",
        genre="Sci-Fi",
        director="James Cameron",
        release_year=2009,
        rating=7.9,
        language="English",
        country="USA",
        duration=162,
        location="Wellington"
    ),
    Movie(
        title="Titanic",
        description="A love story aboard the famous ship.",
        genre="Romance",
        director="James Cameron",
        release_year=1997,
        rating=7.9,
        language="English",
        country="USA",
        duration=195,
        location="Mexico"
    ),
    Movie(
        title="The Matrix",
        description="A hacker discovers the true nature of reality.",
        genre="Sci-Fi",
        director="The Wachowskis",
        release_year=1999,
        rating=8.7,
        language="English",
        country="USA",
        duration=136,
        location="Sydney"
    ),
    Movie(
        title="Gladiator",
        description="A Roman general seeks revenge after betrayal.",
        genre="Action",
        director="Ridley Scott",
        release_year=2000,
        rating=8.5,
        language="English",
        country="USA",
        duration=155,
        location="Malta"
    ),
    Movie(
        title="Parasite",
        description="A poor family becomes involved with a wealthy family.",
        genre="Thriller",
        director="Bong Joon-ho",
        release_year=2019,
        rating=8.5,
        language="Korean",
        country="South Korea",
        duration=132,
        location="Seoul"
    ),
    Movie(
        title="Oppenheimer",
        description="The story of the scientist behind the atomic bomb.",
        genre="Drama",
        director="Christopher Nolan",
        release_year=2023,
        rating=8.6,
        language="English",
        country="USA",
        duration=180,
        location="New Mexico"
    ),
    Movie(
        title="Avengers: Endgame",
        description="The Avengers attempt to undo the events of Infinity War.",
        genre="Action",
        director="Anthony Russo",
        release_year=2019,
        rating=8.4,
        language="English",
        country="USA",
        duration=181,
        location="Atlanta"
    ),
]


db = SessionLocal()

try:
    db.add_all(movies)
    db.commit()
    print("10 movies added successfully!")

finally:
    db.close()