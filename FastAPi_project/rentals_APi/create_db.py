from rentals_api.db.database import engine
from rentals_api.db.base import Base



Base.metadata.create_all(bind=engine)

print("Database tables create successfully")