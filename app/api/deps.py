from fastapi import Depends
from redis.asyncio import Redis

from app.clients.evolution import EvolutionClient
from app.clients.glpi import GLPIClient
from app.core.config import get_settings
from app.core.database import get_db
from app.models.conversation import Base
from app.repositories.conversation import ConversationRepository
from app.services.flow_engine import FlowEngine
from app.services.session import SessionManager
from sqlalchemy.ext.asyncio import AsyncSession

settings = get_settings()


async def get_redis():
    """Dependency that yields a Redis client."""
    client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    try:
        yield client
    finally:
        await client.aclose()


async def get_session_manager(redis: Redis = Depends(get_redis)) -> SessionManager:
    """Dependency that returns a SessionManager instance."""
    return SessionManager(redis, ttl_seconds=settings.SESSION_TTL_SECONDS)


async def get_conversation_repository(
    db: AsyncSession = Depends(get_db),
) -> ConversationRepository:
    """Dependency that returns a ConversationRepository instance."""
    return ConversationRepository(db)


async def get_glpi_client() -> GLPIClient:
    """Dependency that yields a GLPIClient instance."""
    client = GLPIClient(
        base_url=settings.GLPI_URL,
        app_token=settings.GLPI_APP_TOKEN,
        user_token=settings.GLPI_USER_TOKEN,
    )
    try:
        yield client
    finally:
        await client.close()


async def get_evolution_client() -> EvolutionClient:
    """Dependency that yields an EvolutionClient instance."""
    client = EvolutionClient(
        base_url=settings.EVOLUTION_URL,
        api_key=settings.EVOLUTION_API_KEY,
        instance=settings.EVOLUTION_INSTANCE,
    )
    try:
        yield client
    finally:
        await client.close()


async def get_flow_engine(
    glpi: GLPIClient = Depends(get_glpi_client),
    session_manager: SessionManager = Depends(get_session_manager),
) -> FlowEngine:
    """Dependency that returns a FlowEngine instance."""
    return FlowEngine(glpi, session_manager)
