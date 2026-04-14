from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class Step(StrEnum):
    """Estados da máquina de estados do chatbot."""

    WELCOME = "WELCOME"
    AUTH_USERNAME = "AUTH_USERNAME"
    AUTH_PASSWORD = "AUTH_PASSWORD"
    MAIN_MENU = "MAIN_MENU"
    CREATE_TICKET_TITLE = "CREATE_TICKET_TITLE"
    CREATE_TICKET_DESC = "CREATE_TICKET_DESC"
    LIST_TICKETS = "LIST_TICKETS"
    TICKET_STATUS = "TICKET_STATUS"


@dataclass
class FlowResult:
    """Resultado do processamento de uma mensagem pelo motor de fluxo."""

    response_text: str
    next_step: Step
    session_updates: dict = field(default_factory=dict)


class FlowEngine:
    """
    Motor de fluxo do chatbot baseado em máquina de estados.

    Puro — não faz I/O diretamente. Recebe dependências por injeção.
    """

    def __init__(self, glpi_client, session_manager) -> None:
        self._glpi = glpi_client
        self._session = session_manager

    async def process(self, message: str, session: dict) -> FlowResult:
        """
        Processa uma mensagem recebida com base no estado atual da sessão.

        Args:
            message: Texto da mensagem recebida.
            session: Dados da sessão atual (inclui 'step').

        Returns:
            FlowResult com texto de resposta, próximo passo e atualizações de sessão.
        """
        raise NotImplementedError
