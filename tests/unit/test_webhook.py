"""
Testes unitários para o endpoint POST /webhook/evolution.

Usa FastAPI TestClient + mocks de SessionManager, FlowEngine e EvolutionClient.
Todos os testes esperam 500 (NotImplementedError) até a implementação real.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.webhook import WebhookPayload


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def _make_webhook_payload(
    phone: str = "5535999999999",
    message: str = "Olá",
    event: str = "messages.upsert",
) -> dict:
    """Helper para montar payload do webhook."""
    return {
        "event": event,
        "instance": "test-instance",
        "data": {
            "key": {
                "remoteJid": f"{phone}@s.whatsapp.net",
                "fromMe": False,
            },
            "message": {
                "conversation": message,
            },
            "messageType": "conversation",
        },
    }


# ── Testes de Endpoint ───────────────────────────────────────────────


class TestWebhookEndpoint:
    """Testes para POST /webhook/evolution."""

    def test_webhook_receives_valid_payload(self, client):
        """Deve aceitar payload válido (retorna 500 até implementar)."""
        payload = _make_webhook_payload()
        response = client.post("/webhook/evolution", json=payload)
        # Espera 500 porque o handler levanta NotImplementedError
        assert response.status_code == 500

    def test_webhook_receives_empty_message(self, client):
        """Deve aceitar payload com mensagem None."""
        payload = {
            "event": "messages.upsert",
            "instance": "test-instance",
            "data": {
                "key": {"remoteJid": "5535999999999@s.whatsapp.net", "fromMe": False},
                "message": None,
                "messageType": None,
            },
        }
        response = client.post("/webhook/evolution", json=payload)
        assert response.status_code == 500

    def test_webhook_invalid_json(self, client):
        """Deve retornar 422 para JSON inválido."""
        response = client.post(
            "/webhook/evolution",
            content="not json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == 422

    def test_webhook_missing_event(self, client):
        """Deve retornar 422 quando campo 'event' está ausente."""
        payload = {"data": {"key": {"remoteJid": "123@s.whatsapp.net"}}}
        response = client.post("/webhook/evolution", json=payload)
        assert response.status_code == 422

    def test_webhook_from_me_message(self, client):
        """Deve aceitar mensagem enviada pelo próprio bot (fromMe=True)."""
        payload = _make_webhook_payload()
        payload["data"]["key"]["fromMe"] = True
        response = client.post("/webhook/evolution", json=payload)
        assert response.status_code == 500  # aceita, mas NotImplementedError

    def test_webhook_different_event_type(self, client):
        """Deve aceitar eventos diferentes de messages.upsert."""
        payload = _make_webhook_payload(event="connection.update")
        response = client.post("/webhook/evolution", json=payload)
        assert response.status_code == 500


# ── Testes de Schema ─────────────────────────────────────────────────


class TestWebhookPayloadSchema:
    """Testes para o schema WebhookPayload."""

    def test_extract_phone(self):
        """Deve extrair número de telefone do remoteJid."""
        payload = WebhookPayload(**_make_webhook_payload(phone="5535988887777"))
        assert payload.extract_phone() == "5535988887777"

    def test_extract_phone_without_jid_suffix(self):
        """Deve lidar com remoteJid sem @s.whatsapp.net."""
        payload = WebhookPayload(
            event="messages.upsert",
            data={
                "key": {"remoteJid": "5535999999999"},
                "message": {"conversation": "oi"},
            },
        )
        assert payload.extract_phone() == "5535999999999"

    def test_extract_message(self):
        """Deve extrair texto da mensagem."""
        payload = WebhookPayload(**_make_webhook_payload(message="Preciso de ajuda"))
        assert payload.extract_message() == "Preciso de ajuda"

    def test_extract_message_none(self):
        """Deve retornar None quando mensagem está vazia."""
        payload = WebhookPayload(
            event="messages.upsert",
            data={
                "key": {"remoteJid": "5535999999999@s.whatsapp.net"},
                "message": None,
            },
        )
        assert payload.extract_message() is None

    def test_extract_phone_no_data(self):
        """Deve retornar None quando data está ausente."""
        payload = WebhookPayload(event="messages.upsert")
        assert payload.extract_phone() is None

    def test_extract_message_no_data(self):
        """Deve retornar None quando data está ausente."""
        payload = WebhookPayload(event="messages.upsert")
        assert payload.extract_message() is None
