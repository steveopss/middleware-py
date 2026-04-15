from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.api.deps import get_redis
from app.core.database import get_db

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check(
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
):
    """
    Diagnóstico do estado da aplicação e suas dependências.
    """
    health_status = {
        "status": "ok",
        "database": "down",
        "redis": "down",
    }

    # Testar Banco de Dados
    try:
        await db.execute(text("SELECT 1"))
        health_status["database"] = "ok"
    except Exception:
        health_status["status"] = "error"

    # Testar Redis
    try:
        await redis.ping()
        health_status["redis"] = "ok"
    except Exception:
        health_status["status"] = "error"

    return health_status
