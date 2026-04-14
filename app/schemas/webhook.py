from __future__ import annotations

from pydantic import BaseModel


class WebhookKey(BaseModel):
    """Dados da chave do remetente no webhook."""

    remoteJid: str  # Ex: "5535999999999@s.whatsapp.net"
    fromMe: bool = False


class WebhookMessage(BaseModel):
    """Mensagem de texto extraída do webhook."""

    conversation: str | None = None


class WebhookData(BaseModel):
    """Dados principais do evento do webhook."""

    key: WebhookKey
    message: WebhookMessage | None = None
    messageType: str | None = None


class WebhookPayload(BaseModel):
    """
    Payload recebido pelo webhook da Evolution API.

    O formato varia por evento; este schema cobre o evento 'messages.upsert'.
    """

    event: str
    instance: str | None = None
    data: WebhookData | None = None

    def extract_phone(self) -> str | None:
        """Extrai número de telefone do remoteJid (remove @s.whatsapp.net)."""
        if self.data and self.data.key:
            jid = self.data.key.remoteJid
            return jid.split("@")[0] if "@" in jid else jid
        return None

    def extract_message(self) -> str | None:
        """Extrai texto da mensagem."""
        if self.data and self.data.message:
            return self.data.message.conversation
        return None
