from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from rentals_api.db.database import SessionLocal

from .schemas import LocationCreate,LocationRead
from .service import create_location

router=APIRouter(
    prefix='/location',
    tags=["Locations"],
)

def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()

@router.post("/",response_model=LocationRead)
def create_location_endpoint(
    data:LocationCreate,
    db:Session=Depends(get_db)
):
    return create_location(
        db=db,
        data=data,
    )




