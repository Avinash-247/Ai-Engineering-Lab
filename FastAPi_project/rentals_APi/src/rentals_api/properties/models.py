from datetime import date
from decimal import Decimal

from sqlalchemy import ForeignKey,Numeric,String,Text
from sqlalchemy.orm import Mapped,mapped_column

from rentals_api.db.base import Base
from rentals_api.db.mixins import AuditMixin

class Property(AuditMixin,Base):
    __tablename__="properties"

    id:Mapped[int]=mapped_column(primary_key=True)
    location_id:Mapped[int]=mapped_column(
        ForeignKey("locations.id")
    )

    title:Mapped[str]=mapped_column(
        String(100)
    )

    property_type:Mapped[str]=mapped_column(
        String(50)
    )

    furnishing:Mapped[str]=mapped_column(
        String(50)
    )

    bedrooms:Mapped[int]=mapped_column()

    monthly_rent:Mapped[Decimal]=mapped_column(
        Numeric(12,2)
    )

    security_deposit:Mapped[Decimal]=mapped_column(
        Numeric(12,2)
    )

    carpet_area_sqft:Mapped[float]=mapped_column()

    available_from:Mapped[date]=mapped_column()

    status: Mapped[str] =mapped_column(
        String(50),
        default="available."
    )

class PropertyImage(AuditMixin,Base):
    __tablename__="property_images"

    id:Mapped[int]=mapped_column(primary_key=True)

    property_id:Mapped[int]=mapped_column(
        ForeignKey("properties.id")
    )

    url:Mapped[str]=mapped_column(
        String(200)
    )

    position:Mapped[int]=mapped_column(
        default=1
    )


class PropertyAmenity(AuditMixin,Base):
    __tablename__="property_amenities"

    property_id:Mapped[int]=mapped_column(
        ForeignKey("properties.id"),
        primary_key=True,
    )

    amenity_id:Mapped[int] = mapped_column(
        ForeignKey("amenities.id"),
        primary_key=True,
    )










