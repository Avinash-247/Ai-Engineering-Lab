from sqlalchemy import create_engine

Database_url="sqlite:///./expenses.db"

engine=create_engine(Database_url)