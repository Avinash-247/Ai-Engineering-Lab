from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from rentals_api.db.database import SessionLocal

from .schemas import AmenityCreate,AmenityRead
from .service import create_amenity

router =APIRouter(
    prefix="/amenities",
    tags=["Amenities"]
)

def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/",response_model=AmenityRead)
def create_amenity_endpoint(
    data:AmenityCreate,
    db:Session= Depends (get_db)
):
    return create_amenity(
        db=db,
        data=data,
    )
