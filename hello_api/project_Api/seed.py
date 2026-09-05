async def seed_database(db):
    # Movies
    movies = [
        ("Avatar",),
        ("Inception",),
        ("Interstellar",),
        ("KGF",),
    ]

    await db.executemany(
        "INSERT OR IGNORE INTO movies (name) VALUES (?)",
        movies
    )

    # Theaters
    theaters = [
        ("PVR Hyderabad",),
        ("AMB Cinemas",),
        ("INOX Hyderabad",),
        ("Cinepolis Hyderabad",),
    ]

    await db.executemany(
        "INSERT OR IGNORE INTO theaters (name) VALUES (?)",
        theaters
    )

    await db.commit()

    # Get movie IDs
    async with db.execute(
        "SELECT id, name FROM movies"
    ) as cursor:
        movie_rows = await cursor.fetchall()

    # Get theater IDs
    async with db.execute(
        "SELECT id, name FROM theaters"
    ) as cursor:
        theater_rows = await cursor.fetchall()

    movie_ids = {
        row["name"]: row["id"]
        for row in movie_rows
    }

    theater_ids = {
        row["name"]: row["id"]
        for row in theater_rows
    }

    # Movie <-> Theater relationships
    relationships = [
        (movie_ids["Avatar"], theater_ids["PVR Hyderabad"]),
        (movie_ids["Avatar"], theater_ids["AMB Cinemas"]),

        (movie_ids["Inception"], theater_ids["PVR Hyderabad"]),
        (movie_ids["Inception"], theater_ids["INOX Hyderabad"]),

        (movie_ids["Interstellar"], theater_ids["AMB Cinemas"]),
        (movie_ids["Interstellar"], theater_ids["Cinepolis Hyderabad"]),

        (movie_ids["KGF"], theater_ids["PVR Hyderabad"]),
        (movie_ids["KGF"], theater_ids["Cinepolis Hyderabad"]),
    ]

    await db.executemany(
        """
        INSERT OR IGNORE INTO movie_theaters
        (movie_id, theater_id)
        VALUES (?, ?)
        """,
        relationships
    )

    await db.commit()
    