from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.webhook import router as webhook_router


def create_app() -> FastAPI:
    """Application factory."""
    application = FastAPI(
        title="Middleware WhatsApp ↔ GLPI",
        description="Conecta WhatsApp (Evolution API) ao GLPI para gestão de chamados ITSM.",
        version="0.1.0",
    )

    application.include_router(health_router)
    application.include_router(webhook_router)

    return application


app = create_app()
