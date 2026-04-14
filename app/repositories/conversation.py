from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation, Direction


class ConversationRepository:
    """Repositório de persistência para mensagens de conversa."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def save(
        self,
        phone_number: str,
        direction: Direction,
        message: str,
        glpi_ticket_id: int | None = None,
    ) -> Conversation:
        """Salva uma mensagem de conversa."""
        raise NotImplementedError

    async def get_by_phone(self, phone_number: str, limit: int = 50) -> list[Conversation]:
        """Busca mensagens por número de telefone."""
        raise NotImplementedError
