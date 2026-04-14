import enum
import uuid
from datetime import datetime

from sqlalchemy import Enum, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


class Direction(str, enum.Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class Conversation(Base):
    """Log de mensagens para auditoria."""

    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    phone_number: Mapped[str] = mapped_column(String(20), index=True)
    direction: Mapped[Direction] = mapped_column(Enum(Direction))
    message: Mapped[str] = mapped_column(Text)
    glpi_ticket_id: Mapped[int | None] = mapped_column(default=None)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
