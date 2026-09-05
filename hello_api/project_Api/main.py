from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import get_database
from models import create_tables
from seed import seed_database
from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("🚀 Application starting...")

    # 1. Connect to database
    db = await get_database()

    # 2. Store connection in FastAPI state
    app.state.db = db

    # 3. Create tables
    await create_tables(db)

    # 4. Add sample data
    await seed_database(db)

    print("✅ Database connected and initialized")

    # Application runs here
    yield

    # 5. Close database
    await db.close()

    print(" Database connection closed")


app = FastAPI(lifespan=lifespan)

app.include_router(router)


@app.get("/")
async def home():
    return {
        "message": "Movie API is working"
    }