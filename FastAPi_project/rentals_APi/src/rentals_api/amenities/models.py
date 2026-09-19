from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column

from rentals_api.db.base import Base
from rentals_api.db.mixins import AuditMixin

class Amenity(AuditMixin,Base):
    __tablename__="amenities"

    id: Mapped[int]=mapped_column(primary_key=True)

    name:Mapped[str]=mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )