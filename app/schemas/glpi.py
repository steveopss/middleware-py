from __future__ import annotations

from pydantic import BaseModel


class GLPISessionResponse(BaseModel):
    """Resposta do initSession do GLPI."""

    session_token: str


class GLPITicketInput(BaseModel):
    """Dados para criação de um chamado no GLPI."""

    name: str  # título
    content: str  # descrição
    type: int = 1  # 1 = Incident, 2 = Request
    urgency: int = 3  # 1-5
    priority: int = 3  # 1-6


class GLPITicketResponse(BaseModel):
    """Dados resumidos de um chamado retornado pelo GLPI."""

    id: int
    name: str | None = None
    status: int | None = None
    date: str | None = None
    date_mod: str | None = None

    @property
    def status_label(self) -> str:
        """Converte código de status para texto legível."""
        labels = {
            1: "Novo",
            2: "Em atendimento (atribuído)",
            3: "Em atendimento (planejado)",
            4: "Pendente",
            5: "Solucionado",
            6: "Fechado",
        }
        return labels.get(self.status or 0, "Desconhecido")


class GLPIFollowupInput(BaseModel):
    """Dados para adicionar acompanhamento a um chamado."""

    content: str
    is_private: int = 0  # 0 = público
