"""
Testes unitários para EvolutionClient.

Usa respx para mockar todas as chamadas HTTP à Evolution API.
Todos os testes esperam NotImplementedError até a implementação real.
"""

import httpx
import pytest
import respx

from app.clients.evolution import EvolutionClient

EVO_BASE = "http://evolution.test.local"
API_KEY = "test-evo-key"
INSTANCE = "test-instance"


@pytest.fixture
def client() -> EvolutionClient:
    return EvolutionClient(base_url=EVO_BASE, api_key=API_KEY, instance=INSTANCE)


# ── Send Text ────────────────────────────────────────────────────────


class TestSendText:
    """Testes para send_text (POST /message/sendText/{instance})."""

    @respx.mock
    async def test_send_text_success(self, client):
        """Deve enviar mensagem de texto com sucesso."""
        respx.post(f"{EVO_BASE}/message/sendText/{INSTANCE}").mock(
            return_value=httpx.Response(
                200,
                json={"key": {"id": "msg-001"}, "status": "PENDING"},
            )
        )

        with pytest.raises(NotImplementedError):
            await client.send_text("5535999999999", "Olá, como posso ajudar?")

    @respx.mock
    async def test_send_text_includes_apikey_header(self, client):
        """Deve incluir header apikey na requisição."""
        route = respx.post(f"{EVO_BASE}/message/sendText/{INSTANCE}").mock(
            return_value=httpx.Response(200, json={"key": {"id": "msg-002"}})
        )

        with pytest.raises(NotImplementedError):
            await client.send_text("5535999999999", "teste")

    @respx.mock
    async def test_send_text_correct_body(self, client):
        """Deve enviar body com number e text."""
        route = respx.post(f"{EVO_BASE}/message/sendText/{INSTANCE}").mock(
            return_value=httpx.Response(200, json={"key": {"id": "msg-003"}})
        )

        with pytest.raises(NotImplementedError):
            await client.send_text("5535988887777", "Sua mensagem aqui")

    @respx.mock
    async def test_send_text_server_error(self, client):
        """Deve lidar com erro do servidor (500)."""
        respx.post(f"{EVO_BASE}/message/sendText/{INSTANCE}").mock(
            return_value=httpx.Response(500, json={"error": "Internal Server Error"})
        )

        with pytest.raises(NotImplementedError):
            await client.send_text("5535999999999", "teste")


# ── Send Buttons ─────────────────────────────────────────────────────


class TestSendButtons:
    """Testes para send_buttons (POST /message/sendButtons/{instance})."""

    @respx.mock
    async def test_send_buttons_success(self, client):
        """Deve enviar mensagem com botões."""
        respx.post(f"{EVO_BASE}/message/sendButtons/{INSTANCE}").mock(
            return_value=httpx.Response(200, json={"key": {"id": "msg-btn-001"}})
        )

        buttons = [
            {"buttonText": {"displayText": "Abrir chamado"}},
            {"buttonText": {"displayText": "Consultar chamado"}},
        ]

        with pytest.raises(NotImplementedError):
            await client.send_buttons("5535999999999", "Menu Principal", buttons)

    @respx.mock
    async def test_send_buttons_empty_list(self, client):
        """Deve lidar com lista de botões vazia."""
        respx.post(f"{EVO_BASE}/message/sendButtons/{INSTANCE}").mock(
            return_value=httpx.Response(200, json={"key": {"id": "msg-btn-002"}})
        )

        with pytest.raises(NotImplementedError):
            await client.send_buttons("5535999999999", "Menu", [])


# ── Send List ────────────────────────────────────────────────────────


class TestSendList:
    """Testes para send_list (POST /message/sendList/{instance})."""

    @respx.mock
    async def test_send_list_success(self, client):
        """Deve enviar mensagem com lista de opções."""
        respx.post(f"{EVO_BASE}/message/sendList/{INSTANCE}").mock(
            return_value=httpx.Response(200, json={"key": {"id": "msg-list-001"}})
        )

        sections = [
            {
                "title": "Chamados",
                "rows": [
                    {"title": "#10 - Impressora", "description": "Status: Aberto"},
                    {"title": "#11 - Monitor", "description": "Status: Fechado"},
                ],
            }
        ]

        with pytest.raises(NotImplementedError):
            await client.send_list(
                "5535999999999",
                "Seus Chamados",
                "Selecione para ver detalhes",
                sections,
            )


# ── Headers ──────────────────────────────────────────────────────────


class TestBuildHeaders:
    """Testes para _build_headers."""

    def test_headers_include_apikey(self, client):
        """Deve incluir apikey no header."""
        headers = client._build_headers()
        assert headers["apikey"] == API_KEY
        assert headers["Content-Type"] == "application/json"

    def test_headers_no_session_token(self, client):
        """Não deve incluir Session-Token (Evolution não usa)."""
        headers = client._build_headers()
        assert "Session-Token" not in headers
