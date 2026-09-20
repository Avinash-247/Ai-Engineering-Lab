from sqlalchemy.orm import Session

from rentals_api.locations.models import Location
from rentals_api.locations.schemas import LocationCreate

from .models import Property,PropertyAmenity
from .schemas import PropertyCreate


def create_property(
    db:Session,
    data:PropertyCreate
)->Property:

    property=Property(
          location_id=data.location_id,
          title=data.title,
          property_type=data.property_type,
          furnishing=data.frunishing,
          bedrooms=data.bedrooms,
          monthly_rent=data.monthly_rent,
          security_deposit=data.security_deposit,
          carpet_area_sqft=data.carpet_area_sqft,
          available_from=data.available_from,
    )

    db.add(property)
    db.flush() #editional

    for amenity_id in data.amenity_ids:
          property_amenity =PropertyAmenity(
                property_id=property.id,
                amenity_id=amenity_id,
          )
          db.add(property_amenity)
    db.commit()
    db.refresh(property)

    return property






    




