from fastapi import APIRouter

from app.schemas.webhook import WebhookPayload

router = APIRouter(tags=["webhook"])


@router.post("/webhook/evolution")
async def handle_webhook(payload: WebhookPayload):
    """
    Recebe mensagens da Evolution API e processa no flow engine.

    Fluxo:
        1. Extrair phone_number e message do payload
        2. Buscar/criar sessão no Redis
        3. Passar para FlowEngine.process()
        4. Atualizar sessão
        5. Enviar resposta via Evolution client
        6. Retornar 200
    """
    raise NotImplementedError  # TODO: implementar orquestração
