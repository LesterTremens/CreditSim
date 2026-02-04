import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Simulation(Base):
    __tablename__ = "simulations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    annual_rate: Mapped[float] = mapped_column(Numeric(5,2),nullable=False)
    term_months: Mapped[int] = mapped_column(Integer,nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )