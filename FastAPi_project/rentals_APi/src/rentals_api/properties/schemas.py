from datetime import date
from decimal import Decimal

from pydantic import BaseModel,Field

class PropertyCreate(BaseModel):
    location_id:int
    title:str
    property_type:str
    frunishing:str
    bedrooms:int
    monthly_rent:Decimal
    security_deposit:Decimal
    carpet_area_sqft:float | None=None
    available_from:date
    amenity_ids:list[int] = Field(default_factory=list)

class PropertyRead(BaseModel):
    id:int
    location_id:int
    title:str
    property_type:str
    furnishing:str
    bedrooms:int
    monthly_rent:Decimal
    security_deposit:Decimal
    carpet_area_sqft:float|None=None
    available_from:date
    status:str
