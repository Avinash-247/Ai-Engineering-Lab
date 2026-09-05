async def create_tables(db):
    await db.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    await db.execute("""
        CREATE TABLE IF NOT EXISTS theaters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    await db.execute("""
        CREATE TABLE IF NOT EXISTS movie_theaters (
            movie_id INTEGER,
            theater_id INTEGER,
            PRIMARY KEY (movie_id, theater_id),
            FOREIGN KEY (movie_id) REFERENCES movies(id),
            FOREIGN KEY (theater_id) REFERENCES theaters(id)
        )
    """)

    await db.commit()
    