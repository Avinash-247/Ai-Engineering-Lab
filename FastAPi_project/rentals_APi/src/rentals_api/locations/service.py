from sqlalchemy.orm import Session

from .models import Location
from .schemas import LocationCreate


def create_location(
    db: Session,
    data: LocationCreate,
) -> Location:

    location = Location(
        city=data.city,
        locality=data.locality,
        state=data.state,
        description=data.description,
    )

    db.add(location)
    db.commit()
    db.refresh(location)

    return location
