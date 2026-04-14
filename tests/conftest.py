"""
Fixtures globais para todos os testes.

Fornece:
- fake_redis: instância fakeredis para testes de sessão
- glpi_client: GLPIClient configurado com respx mockado
- evolution_client: EvolutionClient configurado com respx mockado
- session_manager: SessionManager com fakeredis
- app_client: AsyncClient do httpx para testes de endpoint
"""

from unittest.mock import AsyncMock

import fakeredis.aioredis
import httpx
import pytest
from fastapi.testclient import TestClient

from app.clients.evolution import EvolutionClient
from app.clients.glpi import GLPIClient
from app.core.config import Settings
from app.main import app
from app.services.session import SessionManager


# ── Settings ──────────────────────────────────────────────────────────


@pytest.fixture
def test_settings() -> Settings:
    """Settings de teste com valores fixos."""
    return Settings(
        APP_ENV="testing",
        DATABASE_URL="sqlite+aiosqlite:///:memory:",
        REDIS_URL="redis://localhost:6379/0",
        SESSION_TTL_SECONDS=300,
        GLPI_URL="https://glpi.test.local/apirest.php",
        GLPI_APP_TOKEN="test-app-token",
        GLPI_USER_TOKEN="test-user-token",
        EVOLUTION_URL="http://evolution.test.local",
        EVOLUTION_API_KEY="test-evo-key",
        EVOLUTION_INSTANCE="test-instance",
    )


# ── Redis ─────────────────────────────────────────────────────────────


@pytest.fixture
async def fake_redis():
    """Instância de fakeredis para testes."""
    server = fakeredis.aioredis.FakeRedis()
    yield server
    await server.aclose()


# ── Session Manager ──────────────────────────────────────────────────


@pytest.fixture
async def session_manager(fake_redis) -> SessionManager:
    """SessionManager com fakeredis."""
    return SessionManager(redis=fake_redis, ttl_seconds=300)


# ── GLPI Client ──────────────────────────────────────────────────────


@pytest.fixture
def glpi_client(test_settings) -> GLPIClient:
    """GLPIClient com URL de teste."""
    return GLPIClient(
        base_url=test_settings.GLPI_URL,
        app_token=test_settings.GLPI_APP_TOKEN,
        user_token=test_settings.GLPI_USER_TOKEN,
    )


# ── Evolution Client ─────────────────────────────────────────────────


@pytest.fixture
def evolution_client(test_settings) -> EvolutionClient:
    """EvolutionClient com URL de teste."""
    return EvolutionClient(
        base_url=test_settings.EVOLUTION_URL,
        api_key=test_settings.EVOLUTION_API_KEY,
        instance=test_settings.EVOLUTION_INSTANCE,
    )


# ── Mock Clients (para testes do flow engine) ────────────────────────


@pytest.fixture
def mock_glpi_client():
    """Mock completo do GLPIClient para testes do FlowEngine."""
    mock = AsyncMock(spec=GLPIClient)
    mock.session_token = None
    return mock


@pytest.fixture
def mock_evolution_client():
    """Mock completo do EvolutionClient para testes do webhook."""
    mock = AsyncMock(spec=EvolutionClient)
    return mock


@pytest.fixture
def mock_session_manager():
    """Mock completo do SessionManager para testes do webhook."""
    mock = AsyncMock(spec=SessionManager)
    return mock


# ── FastAPI Test Client ──────────────────────────────────────────────


@pytest.fixture
def test_app_client() -> TestClient:
    """TestClient síncrono do FastAPI para testes de endpoint."""
    return TestClient(app)
