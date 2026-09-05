from pathlib import Path

import aiosqlite


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "movie" / "movies.db"


async def get_database():
    db = await aiosqlite.connect(DATABASE_PATH)
    db.row_factory = aiosqlite.Row
    return db