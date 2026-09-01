from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Database_url="sqlite:///./expenses.db"

engine=create_engine(Database_url)


SessionLocal=sessionmaker(
    bind=engine
)

