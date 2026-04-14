from __future__ import annotations

import json

from redis.asyncio import Redis


class SessionManager:
    """Gerenciamento de sessão de conversa usando Redis."""

    KEY_PREFIX = "session:"

    def __init__(self, redis: Redis, ttl_seconds: int = 1800) -> None:
        self._redis = redis
        self._ttl = ttl_seconds

    async def get(self, phone: str) -> dict | None:
        """Busca sessão pelo número de telefone. Retorna None se não existir."""
        raise NotImplementedError

    async def set(self, phone: str, data: dict) -> None:
        """Salva ou atualiza sessão com TTL."""
        raise NotImplementedError

    async def delete(self, phone: str) -> None:
        """Remove sessão."""
        raise NotImplementedError

    async def update_step(self, phone: str, step: str) -> None:
        """Atualiza apenas o campo 'step' da sessão existente."""
        raise NotImplementedError

    def _key(self, phone: str) -> str:
        """Gera a chave Redis para o telefone."""
        return f"{self.KEY_PREFIX}{phone}"
