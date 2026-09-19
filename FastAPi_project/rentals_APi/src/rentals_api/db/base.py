from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# class Location(Base):
#     pass

from rentals_api.locations.models import Location
from rentals_api.amenities.models import Amenity
from rentals_api.properties.models import (
    Property, PropertyImage,PropertyAmenity,
)
