from __future__ import annotations

import httpx


class GLPIClient:
    """Client HTTP assíncrono para a API REST do GLPI."""

    def __init__(self, base_url: str, app_token: str, user_token: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.app_token = app_token
        self.user_token = user_token
        self.session_token: str | None = None
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=30.0)

    # ── Auth ──────────────────────────────────────────────────────────

    async def init_session(self) -> str:
        """
        Autentica no GLPI usando user_token + App-Token.
        Retorna e armazena o session_token.
        """
        raise NotImplementedError

    async def kill_session(self) -> None:
        """Encerra a sessão corrente no GLPI."""
        raise NotImplementedError

    # ── Tickets ───────────────────────────────────────────────────────

    async def search_tickets(self, user_id: int | None = None) -> list[dict]:
        """Busca chamados. Filtro opcional por usuário."""
        raise NotImplementedError

    async def get_ticket(self, ticket_id: int) -> dict:
        """Retorna detalhes de um chamado pelo ID."""
        raise NotImplementedError

    async def create_ticket(self, title: str, description: str) -> dict:
        """Cria um novo chamado no GLPI."""
        raise NotImplementedError

    async def add_followup(self, ticket_id: int, content: str) -> dict:
        """Adiciona um acompanhamento (followup) a um chamado existente."""
        raise NotImplementedError

    # ── Auth com login/senha (para fluxo do chatbot) ──────────────────

    async def init_session_with_credentials(self, login: str, password: str) -> str:
        """
        Autentica no GLPI com login e senha do usuário.
        Retorna e armazena o session_token.
        """
        raise NotImplementedError

    # ── Helpers ───────────────────────────────────────────────────────

    def _build_headers(self) -> dict[str, str]:
        """Monta headers padrão com App-Token e Session-Token."""
        headers = {
            "Content-Type": "application/json",
            "App-Token": self.app_token,
        }
        if self.session_token:
            headers["Session-Token"] = self.session_token
        return headers

    async def close(self) -> None:
        """Fecha o client HTTP."""
        await self._client.aclose()
