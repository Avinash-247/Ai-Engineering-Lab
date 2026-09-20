from fastapi import APIRouter

from rentals_api.locations.router import router as location_router
from rentals_api.amenities.router import router as amenities_router
from rentals_api.properties.router import router as property_router

router=APIRouter(
    prefix="/api/vi",
)

router.include_router(location_router)
router.include_router(amenities_router)
router.include_router(property_router)

