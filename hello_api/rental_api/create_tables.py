from app.database.connection import engine,Base
from app.models.movie import Movie


Base.metadata.create_all(bind=engine)

print("table created")