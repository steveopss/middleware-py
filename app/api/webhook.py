from fastapi import APIRouter, Depends
from app.api.deps import (
    get_evolution_client,
    get_flow_engine,
    get_session_manager,
    get_conversation_repository,
)
from app.schemas.webhook import WebhookPayload
from app.models.conversation import Direction
from app.repositories.conversation import ConversationRepository

router = APIRouter(tags=["webhook"])


@router.post("/webhook/evolution")
async def handle_webhook(
    payload: WebhookPayload,
    flow_engine=Depends(get_flow_engine),
    session_manager=Depends(get_session_manager),
    evolution_client=Depends(get_evolution_client),
    repo: ConversationRepository = Depends(get_conversation_repository),
):
    """
    Recebe mensagens da Evolution API e processa no flow engine.
    """
    # 1. Filtros básicos
    if payload.event != "messages.upsert":
        return {"status": "ignored", "reason": "not a message event"}

    if payload.data and payload.data.key.fromMe:
        return {"status": "ignored", "reason": "message from me"}

    phone = payload.extract_phone()
    message = payload.extract_message() or ""

    if not phone:
        return {"status": "error", "reason": "phone_not_found"}

    # 2. Gerenciamento de sessão
    session_data = await session_manager.get(phone) or {}

    # PERSISTÊNCIA: Salva mensagem de entrada
    await repo.save(
        phone_number=phone,
        direction=Direction.INBOUND,
        message=message or "",
        glpi_ticket_id=session_data.get("glpi_ticket_id"),
    )

    # 3. Processamento no motor de fluxo
    result = await flow_engine.process(message, session_data)

    # 4. Persistência de estado
    new_session_data = {**session_data, **result.session_updates}
    new_session_data["step"] = result.next_step
    await session_manager.set(phone, new_session_data)

    # PERSISTÊNCIA: Salva mensagem de saída
    await repo.save(
        phone_number=phone,
        direction=Direction.OUTBOUND,
        message=result.response_text or "",
        glpi_ticket_id=new_session_data.get("glpi_ticket_id"),
    )

    # 5. Resposta via Evolution API
    await evolution_client.send_text(phone, result.response_text)

    return {"status": "success"}
