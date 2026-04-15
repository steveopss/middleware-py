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
        conversation = Conversation(
            phone_number=phone_number,
            direction=direction,
            message=message,
            glpi_ticket_id=glpi_ticket_id,
        )
        self._db.add(conversation)
        await self._db.commit()
        await self._db.refresh(conversation)
        return conversation

    async def get_by_phone(self, phone_number: str, limit: int = 50) -> list[Conversation]:
        """Busca mensagens por número de telefone."""
        query = (
            select(Conversation)
            .where(Conversation.phone_number == phone_number)
            .order_by(Conversation.created_at.desc())
            .limit(limit)
        )
        result = await self._db.execute(query)
        return list(result.scalars().all())
