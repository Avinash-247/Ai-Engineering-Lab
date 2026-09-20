from fastapi import FastAPI

from rentals_api.api.router import router

app=FastAPI(
    title="Rentals_APi"
) 

app.include_router(router)
