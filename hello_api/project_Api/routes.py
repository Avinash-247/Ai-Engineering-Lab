from fastapi import APIRouter, Depends, HTTPException, Request


router = APIRouter()


def get_db(request: Request):
    return request.app.state.db


@router.get("/movies/{movie_name}")
async def get_movie_theaters(
    movie_name: str,
    db=Depends(get_db)
):
    query = """
        SELECT theaters.name
        FROM movies
        JOIN movie_theaters
            ON movies.id = movie_theaters.movie_id
        JOIN theaters
            ON theaters.id = movie_theaters.theater_id
        WHERE movies.name = ?
    """

    async with db.execute(query, (movie_name,)) as cursor:
        rows = await cursor.fetchall()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="Movie not found or no theaters available"
        )

    return {
        "movie": movie_name,
        "theaters": [row["name"] for row in rows]
    }


@router.get("/theaters/{theater_name}")
async def get_theater_movies(
    theater_name: str,
    db=Depends(get_db)
):
    query = """
        SELECT movies.name
        FROM theaters
        JOIN movie_theaters
            ON theaters.id = movie_theaters.theater_id
        JOIN movies
            ON movies.id = movie_theaters.movie_id
        WHERE theaters.name = ?
    """

    async with db.execute(query, (theater_name,)) as cursor:
        rows = await cursor.fetchall()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="Theater not found or no movies available"
        )

    return {
        "theater": theater_name,
        "movies": [row["name"] for row in rows]
    }