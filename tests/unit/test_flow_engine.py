"""
Testes unitários para FlowEngine.

Usa mocks de GLPIClient e SessionManager para isolar a lógica de fluxo.
Todos os testes esperam NotImplementedError até a implementação real.
"""

from unittest.mock import AsyncMock

import pytest

from app.services.flow_engine import FlowEngine, FlowResult, Step


@pytest.fixture
def flow_engine(mock_glpi_client, mock_session_manager):
    """FlowEngine com dependências mockadas."""
    return FlowEngine(glpi_client=mock_glpi_client, session_manager=mock_session_manager)


# ── Estado WELCOME ───────────────────────────────────────────────────


class TestWelcomeStep:
    """Testes para o estado WELCOME."""

    async def test_welcome_sends_greeting(self, flow_engine):
        """Deve enviar mensagem de boas-vindas."""
        session = {"step": Step.WELCOME}

        with pytest.raises(NotImplementedError):
            result = await flow_engine.process("oi", session)

    async def test_welcome_transitions_to_auth_username(self, flow_engine):
        """Deve transicionar para AUTH_USERNAME."""
        session = {"step": Step.WELCOME}

        with pytest.raises(NotImplementedError):
            result = await flow_engine.process("qualquer coisa", session)


# ── Estado AUTH_USERNAME ─────────────────────────────────────────────


class TestAuthUsernameStep:
    """Testes para o estado AUTH_USERNAME."""

    async def test_saves_login_in_session(self, flow_engine):
        """Deve salvar o login informado na sessão."""
        session = {"step": Step.AUTH_USERNAME}

        with pytest.raises(NotImplementedError):
            result = await flow_engine.process("joao.silva", session)

    async def test_transitions_to_auth_password(self, flow_engine):
        """Deve transicionar para AUTH_PASSWORD."""
        session = {"step": Step.AUTH_USERNAME}

        with pytest.raises(NotImplementedError):
            result = await flow_engine.process("joao.silva", session)

    async def test_asks_for_password(self, flow_engine):
        """Deve pedir a senha ao usuário."""
        session = {"step": Step.AUTH_USERNAME}

        with pytest.raises(NotImplementedError):
            result = await flow_engine.process("joao.silva", session)


# ── Estado AUTH_PASSWORD ─────────────────────────────────────────────


class TestAuthPasswordStep:
    """Testes para o estado AUTH_PASSWORD."""

    async def test_successful_login(self, flow_engine, mock_glpi_client):
        """Deve autenticar com sucesso e ir para MAIN_MENU."""
        mock_glpi_client.init_session_with_credentials.return_value = "session-token-123"
        session = {"step": Step.AUTH_PASSWORD, "login": "joao.silva"}

        with pytest.raises(NotImplementedError):
            result = await flow_engine.process("senha123", session)

    async def test_failed_login(self, flow_engine, mock_glpi_client):
        """Deve voltar para AUTH_USERNAME quando login falha."""
        mock_glpi_client.init_session_with_credentials.side_effect = Exception("Login failed")
        session = {"step": Step.AUTH_PASSWORD, "login": "joao.silva"}

        with pytest.raises(NotImplementedError):
            result = await flow_engine.process("senha-errada", session)

    async def test_failed_login_sends_error_message(self, flow_engine, mock_glpi_client):
        """Deve informar o usuário sobre falha no login."""
        mock_glpi_client.init_session_with_credentials.side_effect = Exception("Login failed")
        session = {"step": Step.AUTH_PASSWORD, "login": "joao.silva"}

        with pytest.raises(NotImplementedError):
            result = await flow_engine.process("senha-errada", session)


# ── Estado MAIN_MENU ─────────────────────────────────────────────────


class TestMainMenuStep:
    """Testes para o estado MAIN_MENU."""

    async def test_option_1_goes_to_create_ticket(self, flow_engine):
        """Opção 1 deve transicionar para CREATE_TICKET_TITLE."""
        session = {"step": Step.MAIN_MENU, "authenticated": True}

        with pytest.raises(NotImplementedError):
            result = await flow_engine.process("1", session)

    async def test_option_2_lists_tickets(self, flow_engine, mock_glpi_client):
        """Opção 2 deve buscar e listar chamados."""
        mock_glpi_client.search_tickets.return_value = [
            {"id": 10, "name": "Chamado A", "status": 1},
            {"id": 11, "name": "Chamado B", "status": 5},
        ]
        session = {"step": Step.MAIN_MENU, "authenticated": True, "glpi_session_token": "tok"}

        with pytest.raises(NotImplementedError):
            result = await flow_engine.process("2", session)

    async def test_option_2_empty_list(self, flow_engine, mock_glpi_client):
        """Opção 2 sem chamados deve informar que não há chamados."""
        mock_glpi_client.search_tickets.return_value = []
        session = {"step": Step.MAIN_MENU, "authenticated": True, "glpi_session_token": "tok"}

        with pytest.raises(NotImplementedError):
            result = await flow_engine.process("2", session)

    async def test_option_3_goes_to_ticket_status(self, flow_engine):
        """Opção 3 deve transicionar para TICKET_STATUS."""
        session = {"step": Step.MAIN_MENU, "authenticated": True}

        with pytest.raises(NotImplementedError):
            result = await flow_engine.process("3", session)

    async def test_invalid_option(self, flow_engine):
        """Opção inválida deve pedir para escolher novamente."""
        session = {"step": Step.MAIN_MENU, "authenticated": True}

        with pytest.raises(NotImplementedError):
            result = await flow_engine.process("99", session)

    async def test_text_option(self, flow_engine):
        """Texto livre deve ser tratado como opção inválida."""
        session = {"step": Step.MAIN_MENU, "authenticated": True}

        with pytest.raises(NotImplementedError):
            result = await flow_engine.process("quero abrir um chamado", session)


# ── Estado CREATE_TICKET_TITLE ───────────────────────────────────────


class TestCreateTicketTitleStep:
    """Testes para o estado CREATE_TICKET_TITLE."""

    async def test_saves_title_and_goes_to_desc(self, flow_engine):
        """Deve salvar o título e transicionar para CREATE_TICKET_DESC."""
        session = {"step": Step.CREATE_TICKET_TITLE}

        with pytest.raises(NotImplementedError):
            result = await flow_engine.process("Impressora não funciona", session)

    async def test_asks_for_description(self, flow_engine):
        """Deve pedir a descrição do chamado."""
        session = {"step": Step.CREATE_TICKET_TITLE}

        with pytest.raises(NotImplementedError):
            result = await flow_engine.process("Monitor apagado", session)


# ── Estado CREATE_TICKET_DESC ────────────────────────────────────────


class TestCreateTicketDescStep:
    """Testes para o estado CREATE_TICKET_DESC."""

    async def test_creates_ticket_and_goes_to_menu(self, flow_engine, mock_glpi_client):
        """Deve criar chamado no GLPI e voltar ao MAIN_MENU."""
        mock_glpi_client.create_ticket.return_value = {"id": 42}
        session = {
            "step": Step.CREATE_TICKET_DESC,
            "ticket_title": "Impressora não funciona",
            "glpi_session_token": "tok",
        }

        with pytest.raises(NotImplementedError):
            result = await flow_engine.process(
                "A impressora do 2o andar parou de imprimir desde ontem.", session
            )

    async def test_ticket_creation_failure(self, flow_engine, mock_glpi_client):
        """Deve informar erro quando criação de chamado falha."""
        mock_glpi_client.create_ticket.side_effect = Exception("GLPI Error")
        session = {
            "step": Step.CREATE_TICKET_DESC,
            "ticket_title": "Teste",
            "glpi_session_token": "tok",
        }

        with pytest.raises(NotImplementedError):
            result = await flow_engine.process("Descrição", session)

    async def test_response_includes_ticket_id(self, flow_engine, mock_glpi_client):
        """Resposta deve incluir o número do chamado criado."""
        mock_glpi_client.create_ticket.return_value = {"id": 99}
        session = {
            "step": Step.CREATE_TICKET_DESC,
            "ticket_title": "Teste",
            "glpi_session_token": "tok",
        }

        with pytest.raises(NotImplementedError):
            result = await flow_engine.process("Descrição do problema", session)


# ── Estado TICKET_STATUS ─────────────────────────────────────────────


class TestTicketStatusStep:
    """Testes para o estado TICKET_STATUS."""

    async def test_shows_ticket_status(self, flow_engine, mock_glpi_client):
        """Deve mostrar status do chamado e voltar ao menu."""
        mock_glpi_client.get_ticket.return_value = {
            "id": 10,
            "name": "Impressora quebrada",
            "status": 2,
            "date": "2026-04-14 09:00:00",
        }
        session = {"step": Step.TICKET_STATUS, "glpi_session_token": "tok"}

        with pytest.raises(NotImplementedError):
            result = await flow_engine.process("10", session)

    async def test_ticket_not_found(self, flow_engine, mock_glpi_client):
        """Deve informar quando chamado não existe."""
        mock_glpi_client.get_ticket.side_effect = Exception("Not found")
        session = {"step": Step.TICKET_STATUS, "glpi_session_token": "tok"}

        with pytest.raises(NotImplementedError):
            result = await flow_engine.process("999", session)

    async def test_invalid_ticket_number(self, flow_engine):
        """Deve lidar com entrada que não é número."""
        session = {"step": Step.TICKET_STATUS}

        with pytest.raises(NotImplementedError):
            result = await flow_engine.process("abc", session)


# ── Step Enum ────────────────────────────────────────────────────────


class TestStepEnum:
    """Testes para o enum Step."""

    def test_all_steps_exist(self):
        """Deve ter todos os estados definidos."""
        expected = {
            "WELCOME",
            "AUTH_USERNAME",
            "AUTH_PASSWORD",
            "MAIN_MENU",
            "CREATE_TICKET_TITLE",
            "CREATE_TICKET_DESC",
            "LIST_TICKETS",
            "TICKET_STATUS",
        }
        assert set(Step.__members__.keys()) == expected

    def test_step_values_are_strings(self):
        """Valores do enum devem ser strings."""
        for step in Step:
            assert isinstance(step.value, str)


# ── FlowResult ───────────────────────────────────────────────────────


class TestFlowResult:
    """Testes para o dataclass FlowResult."""

    def test_create_flow_result(self):
        """Deve criar FlowResult com todos os campos."""
        result = FlowResult(
            response_text="Olá!",
            next_step=Step.AUTH_USERNAME,
            session_updates={"login": "teste"},
        )
        assert result.response_text == "Olá!"
        assert result.next_step == Step.AUTH_USERNAME
        assert result.session_updates == {"login": "teste"}

    def test_default_session_updates(self):
        """session_updates deve ser dict vazio por padrão."""
        result = FlowResult(response_text="Test", next_step=Step.WELCOME)
        assert result.session_updates == {}
