from __future__ import annotations

import httpx


class EvolutionClient:
    """Client HTTP assíncrono para a Evolution API (WhatsApp)."""

    def __init__(self, base_url: str, api_key: str, instance: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.instance = instance
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=30.0)

    async def send_text(self, number: str, text: str) -> dict:
        """
        Envia uma mensagem de texto simples.

        POST /message/sendText/{instance}
        Body: {"number": "...", "text": "..."}
        """
        raise NotImplementedError

    async def send_buttons(
        self, number: str, title: str, buttons: list[dict]
    ) -> dict:
        """
        Envia mensagem com botões interativos.

        POST /message/sendButtons/{instance}
        """
        raise NotImplementedError

    async def send_list(
        self, number: str, title: str, description: str, sections: list[dict]
    ) -> dict:
        """
        Envia mensagem com lista de opções.

        POST /message/sendList/{instance}
        """
        raise NotImplementedError

    def _build_headers(self) -> dict[str, str]:
        """Monta headers padrão com apikey."""
        return {
            "Content-Type": "application/json",
            "apikey": self.api_key,
        }

    async def close(self) -> None:
        """Fecha o client HTTP."""
        await self._client.aclose()
