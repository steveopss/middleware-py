"""
Testes unitários para SessionManager.

Usa fakeredis para mockar Redis.
Todos os testes esperam NotImplementedError até a implementação real.
"""

import json

import pytest

from app.services.session import SessionManager


# ── Get ──────────────────────────────────────────────────────────────


class TestGet:
    """Testes para SessionManager.get()."""

    async def test_get_existing_session(self, session_manager, fake_redis):
        """Deve retornar dados da sessão quando existe."""
        session_data = {"step": "MAIN_MENU", "authenticated": True, "login": "joao"}
        await fake_redis.set("session:5535999999999", json.dumps(session_data))

        with pytest.raises(NotImplementedError):
            await session_manager.get("5535999999999")

    async def test_get_nonexistent_session(self, session_manager):
        """Deve retornar None quando sessão não existe."""
        with pytest.raises(NotImplementedError):
            await session_manager.get("5535000000000")

    async def test_get_expired_session(self, session_manager, fake_redis):
        """Deve retornar None quando sessão expirou (TTL)."""
        await fake_redis.set("session:5535111111111", json.dumps({"step": "WELCOME"}))
        # Simular expiração manualmente
        await fake_redis.delete("session:5535111111111")

        with pytest.raises(NotImplementedError):
            await session_manager.get("5535111111111")


# ── Set ──────────────────────────────────────────────────────────────


class TestSet:
    """Testes para SessionManager.set()."""

    async def test_set_new_session(self, session_manager, fake_redis):
        """Deve salvar nova sessão no Redis."""
        session_data = {"step": "WELCOME", "authenticated": False}

        with pytest.raises(NotImplementedError):
            await session_manager.set("5535999999999", session_data)

    async def test_set_overwrites_existing(self, session_manager, fake_redis):
        """Deve sobrescrever sessão existente."""
        await fake_redis.set(
            "session:5535999999999",
            json.dumps({"step": "WELCOME"}),
        )

        with pytest.raises(NotImplementedError):
            await session_manager.set("5535999999999", {"step": "MAIN_MENU"})

    async def test_set_applies_ttl(self, session_manager, fake_redis):
        """Deve configurar TTL na chave."""
        with pytest.raises(NotImplementedError):
            await session_manager.set("5535999999999", {"step": "WELCOME"})


# ── Delete ───────────────────────────────────────────────────────────


class TestDelete:
    """Testes para SessionManager.delete()."""

    async def test_delete_existing_session(self, session_manager, fake_redis):
        """Deve remover sessão existente."""
        await fake_redis.set("session:5535999999999", json.dumps({"step": "WELCOME"}))

        with pytest.raises(NotImplementedError):
            await session_manager.delete("5535999999999")

    async def test_delete_nonexistent_session(self, session_manager):
        """Deve ser idempotente para sessão inexistente."""
        with pytest.raises(NotImplementedError):
            await session_manager.delete("5535000000000")


# ── Update Step ──────────────────────────────────────────────────────


class TestUpdateStep:
    """Testes para SessionManager.update_step()."""

    async def test_update_step_success(self, session_manager, fake_redis):
        """Deve atualizar apenas o campo step sem alterar outros dados."""
        session_data = {"step": "WELCOME", "login": "joao", "authenticated": False}
        await fake_redis.set("session:5535999999999", json.dumps(session_data))

        with pytest.raises(NotImplementedError):
            await session_manager.update_step("5535999999999", "AUTH_USERNAME")

    async def test_update_step_nonexistent_session(self, session_manager):
        """Deve lidar com sessão inexistente ao atualizar step."""
        with pytest.raises(NotImplementedError):
            await session_manager.update_step("5535000000000", "WELCOME")


# ── Key ──────────────────────────────────────────────────────────────


class TestKey:
    """Testes para SessionManager._key()."""

    def test_key_format(self, session_manager):
        """Deve gerar chave no formato session:{phone}."""
        assert session_manager._key("5535999999999") == "session:5535999999999"

    def test_key_prefix(self, session_manager):
        """Deve usar o prefixo correto."""
        assert session_manager._key("123").startswith("session:")
