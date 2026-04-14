from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check():
    """Liveness / readiness probe."""
    raise NotImplementedError  # TODO: implementar checagem de Redis, DB e GLPI
