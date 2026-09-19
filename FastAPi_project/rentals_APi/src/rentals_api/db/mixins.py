from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped,mapped_column
class AuditMixin:
    update_by:Mapped[int|None]=mapped_column(nullable=True)
    update_at:Mapped[datetime]=mapped_column(
        DateTime,
        server_default="CURRENT_TIMESTAMP",
    )
    update_by:Mapped[int|None]=mapped_column(nullable=True)
    update_at:Mapped[datetime]=mapped_column(
        DateTime,
        server_default="CURRENT_TIMESTAMP",
    )
