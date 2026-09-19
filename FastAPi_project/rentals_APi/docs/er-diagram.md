             FastAPI
                │
                ↓
        SQLAlchemy Models
                │
                ↓
          PostgreSQL DB
                │
       ┌────────┼────────┐
       ↓        ↓        ↓
  locations  amenities properties
                         │
                    ┌────┴────┐
                    ↓         ↓
             property_images
             property_amenities