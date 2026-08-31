from expenses.database import engine
from expenses.model import Base

Base.metadata.create_all(engine)

print("Database created")