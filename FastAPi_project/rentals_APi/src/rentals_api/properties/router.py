from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from rentals_api.db.database import SessionLocal
from .service import create_property
from .schemas import PropertyCreate,PropertyRead

router=APIRouter(
    prefix='/properties',
    tags=['Properties']
)

def get_db():
    db=SessionLocal()

    try:
        yield db
    finally:
        db.close()

@router.post("/",response_model=PropertyRead)
def create_property_endpoint(
    data:PropertyCreate,
    db:Session=Depends(get_db)
):
    return create_property(
        db=db,
        data=data,
    )
