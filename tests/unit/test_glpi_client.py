"""
Testes unitários para GLPIClient.

Usa respx para mockar todas as chamadas HTTP ao GLPI REST API.
Todos os testes esperam NotImplementedError até a implementação real.
"""

import httpx
import pytest
import respx

from app.clients.glpi import GLPIClient

GLPI_BASE = "https://glpi.test.local/apirest.php"
APP_TOKEN = "test-app-token"
USER_TOKEN = "test-user-token"


@pytest.fixture
def client() -> GLPIClient:
    return GLPIClient(base_url=GLPI_BASE, app_token=APP_TOKEN, user_token=USER_TOKEN)


# ── Testes de Autenticação ───────────────────────────────────────────


class TestInitSession:
    """Testes para init_session (GET /initSession)."""

    @respx.mock
    async def test_init_session_success(self, client):
        """Deve retornar e armazenar session_token quando login é bem-sucedido."""
        respx.get(f"{GLPI_BASE}/initSession").mock(
            return_value=httpx.Response(
                200,
                json={"session_token": "abc123"},
            )
        )

        with pytest.raises(NotImplementedError):
            await client.init_session()

    @respx.mock
    async def test_init_session_invalid_credentials(self, client):
        """Deve levantar exceção quando credenciais são inválidas (401)."""
        respx.get(f"{GLPI_BASE}/initSession").mock(
            return_value=httpx.Response(401, json=["ERROR_GLPI_LOGIN"])
        )

        with pytest.raises(NotImplementedError):
            await client.init_session()

    @respx.mock
    async def test_init_session_stores_token(self, client):
        """Após init_session, session_token deve estar disponível no client."""
        respx.get(f"{GLPI_BASE}/initSession").mock(
            return_value=httpx.Response(200, json={"session_token": "stored-token"})
        )

        # Quando implementado, o client deve armazenar o token
        assert client.session_token is None  # antes da chamada

        with pytest.raises(NotImplementedError):
            await client.init_session()


class TestInitSessionWithCredentials:
    """Testes para init_session_with_credentials (login/senha via chat)."""

    @respx.mock
    async def test_login_with_valid_credentials(self, client):
        """Deve autenticar com login e senha do usuário (Basic Auth)."""
        respx.get(f"{GLPI_BASE}/initSession").mock(
            return_value=httpx.Response(200, json={"session_token": "user-session-123"})
        )

        with pytest.raises(NotImplementedError):
            await client.init_session_with_credentials("joao.silva", "senha123")

    @respx.mock
    async def test_login_with_wrong_password(self, client):
        """Deve falhar quando senha está incorreta."""
        respx.get(f"{GLPI_BASE}/initSession").mock(
            return_value=httpx.Response(
                401,
                json=["ERROR_GLPI_LOGIN", ""],
            )
        )

        with pytest.raises(NotImplementedError):
            await client.init_session_with_credentials("joao.silva", "senha-errada")


class TestKillSession:
    """Testes para kill_session (GET /killSession)."""

    @respx.mock
    async def test_kill_session_success(self, client):
        """Deve encerrar sessão com sucesso."""
        client.session_token = "abc123"
        respx.get(f"{GLPI_BASE}/killSession").mock(
            return_value=httpx.Response(200)
        )

        with pytest.raises(NotImplementedError):
            await client.kill_session()

    @respx.mock
    async def test_kill_session_clears_token(self, client):
        """Após kill, session_token deve ser None."""
        client.session_token = "abc123"
        respx.get(f"{GLPI_BASE}/killSession").mock(
            return_value=httpx.Response(200)
        )

        with pytest.raises(NotImplementedError):
            await client.kill_session()


# ── Testes de Tickets ────────────────────────────────────────────────


class TestSearchTickets:
    """Testes para search_tickets (GET /search/Ticket)."""

    @respx.mock
    async def test_search_tickets_returns_list(self, client):
        """Deve retornar lista de tickets."""
        client.session_token = "valid-token"
        respx.get(f"{GLPI_BASE}/search/Ticket").mock(
            return_value=httpx.Response(
                200,
                json={
                    "totalcount": 2,
                    "count": 2,
                    "data": [
                        {"1": 10, "2": "Chamado A"},
                        {"1": 11, "2": "Chamado B"},
                    ],
                },
            )
        )

        with pytest.raises(NotImplementedError):
            await client.search_tickets()

    @respx.mock
    async def test_search_tickets_empty(self, client):
        """Deve retornar lista vazia quando não há tickets."""
        client.session_token = "valid-token"
        respx.get(f"{GLPI_BASE}/search/Ticket").mock(
            return_value=httpx.Response(
                200,
                json={"totalcount": 0, "count": 0, "data": []},
            )
        )

        with pytest.raises(NotImplementedError):
            await client.search_tickets()

    @respx.mock
    async def test_search_tickets_with_user_filter(self, client):
        """Deve filtrar tickets por user_id quando fornecido."""
        client.session_token = "valid-token"
        respx.get(f"{GLPI_BASE}/search/Ticket").mock(
            return_value=httpx.Response(
                200,
                json={"totalcount": 1, "count": 1, "data": [{"1": 10, "2": "Chamado A"}]},
            )
        )

        with pytest.raises(NotImplementedError):
            await client.search_tickets(user_id=42)


class TestGetTicket:
    """Testes para get_ticket (GET /Ticket/{id})."""

    @respx.mock
    async def test_get_ticket_success(self, client):
        """Deve retornar detalhes do ticket."""
        client.session_token = "valid-token"
        respx.get(f"{GLPI_BASE}/Ticket/10").mock(
            return_value=httpx.Response(
                200,
                json={
                    "id": 10,
                    "name": "Problema com impressora",
                    "status": 1,
                    "date": "2026-04-14 09:00:00",
                },
            )
        )

        with pytest.raises(NotImplementedError):
            await client.get_ticket(10)

    @respx.mock
    async def test_get_ticket_not_found(self, client):
        """Deve lidar com ticket não encontrado (404)."""
        client.session_token = "valid-token"
        respx.get(f"{GLPI_BASE}/Ticket/999").mock(
            return_value=httpx.Response(
                400,
                json=["ERROR_ITEM_NOT_FOUND", ""],
            )
        )

        with pytest.raises(NotImplementedError):
            await client.get_ticket(999)


class TestCreateTicket:
    """Testes para create_ticket (POST /Ticket)."""

    @respx.mock
    async def test_create_ticket_success(self, client):
        """Deve criar ticket e retornar o ID."""
        client.session_token = "valid-token"
        respx.post(f"{GLPI_BASE}/Ticket").mock(
            return_value=httpx.Response(
                201,
                json={"id": 42, "message": ""},
            )
        )

        with pytest.raises(NotImplementedError):
            await client.create_ticket(
                title="Monitor não liga",
                description="O monitor do setor financeiro não liga desde hoje cedo.",
            )

    @respx.mock
    async def test_create_ticket_sends_correct_payload(self, client):
        """Deve enviar input com name e content no payload."""
        client.session_token = "valid-token"

        route = respx.post(f"{GLPI_BASE}/Ticket").mock(
            return_value=httpx.Response(201, json={"id": 43})
        )

        with pytest.raises(NotImplementedError):
            await client.create_ticket(
                title="Teste",
                description="Descrição do teste",
            )


class TestAddFollowup:
    """Testes para add_followup (POST /Ticket/{id}/ITILFollowup)."""

    @respx.mock
    async def test_add_followup_success(self, client):
        """Deve adicionar acompanhamento ao ticket."""
        client.session_token = "valid-token"
        respx.post(f"{GLPI_BASE}/Ticket/10/ITILFollowup").mock(
            return_value=httpx.Response(201, json={"id": 100})
        )

        with pytest.raises(NotImplementedError):
            await client.add_followup(10, "Atualização: técnico a caminho.")


# ── Testes de Headers ────────────────────────────────────────────────


class TestBuildHeaders:
    """Testes para _build_headers."""

    def test_headers_without_session(self, client):
        """Deve incluir App-Token mas não Session-Token."""
        headers = client._build_headers()
        assert headers["App-Token"] == APP_TOKEN
        assert "Session-Token" not in headers
        assert headers["Content-Type"] == "application/json"

    def test_headers_with_session(self, client):
        """Deve incluir App-Token e Session-Token."""
        client.session_token = "session-xyz"
        headers = client._build_headers()
        assert headers["App-Token"] == APP_TOKEN
        assert headers["Session-Token"] == "session-xyz"
