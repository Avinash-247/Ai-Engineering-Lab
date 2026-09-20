from sqlalchemy.orm import Session

from rentals_api.amenities.models import Amenity
from rentals_api.amenities.schemas import AmenityCreate

def create_amenity(
    db:Session,
    data:AmenityCreate
)->Amenity:

    amenity=Amenity(
        name=data.name,
    )

    db.add(amenity)
    db.commit()
    db.refresh(amenity)

    return amenity