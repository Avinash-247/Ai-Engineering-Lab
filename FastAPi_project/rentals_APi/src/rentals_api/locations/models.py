from sqlalchemy import String,Text
from sqlalchemy.orm import Mapped,mapped_column

from rentals_api.db.base import Base
from rentals_api.db.mixins import AuditMixin

class Location(AuditMixin,Base):
    __tablename__="locations"

    id:Mapped[int]=mapped_column(primary_key=True)
    city:Mapped[str]=mapped_column(String(100))
    locality:Mapped[str]=mapped_column(String(100))
    state:Mapped[str]=mapped_column(String(20))
    description:Mapped[str|None] = mapped_column(Text,nullable=True)



