import asyncio
import json
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from fastapi import HTTPException

from backend.ai import groq_service
from backend.ai.groq_service import AIProviderError
from backend.models.dataset import Dataset
from backend.routes import ai as ai_routes
from backend.routes.dataset import _get_owned_dataset
from backend.utils.exceptions import generic_exception_handler


def test_generic_exception_handler_does_not_expose_internal_details():
    response = asyncio.run(
        generic_exception_handler(
            Mock(),
            RuntimeError("postgres://internal-host/private-database"),
        )
    )

    payload = json.loads(response.body)
    assert response.status_code == 500
    assert payload == {
        "success": False,
        "message": "An unexpected server error occurred.",
    }


def test_groq_provider_error_is_wrapped_without_leaking_provider_details(monkeypatch):
    class BrokenCompletions:
        def create(self, **kwargs):
            raise RuntimeError("provider-secret-token")

    fake_client = SimpleNamespace(
        chat=SimpleNamespace(completions=BrokenCompletions())
    )
    monkeypatch.setattr(groq_service, "client", fake_client)

    with pytest.raises(AIProviderError) as error:
        groq_service.ask_ai("Summarize the business.", analysis={})

    assert str(error.value) == "AI provider request failed."
    assert "provider-secret-token" not in str(error.value)


def test_dataset_owner_helper_rejects_another_users_dataset():
    session = Mock()
    session.get.return_value = SimpleNamespace(id=42, user_id=200)

    with pytest.raises(HTTPException) as error:
        _get_owned_dataset(42, SimpleNamespace(id=100), session)

    assert error.value.status_code == 403
    assert error.value.detail == "Access denied."


def test_dataset_owner_helper_returns_404_for_missing_dataset():
    session = Mock()
    session.get.return_value = None

    with pytest.raises(HTTPException) as error:
        _get_owned_dataset(42, SimpleNamespace(id=100), session)

    assert error.value.status_code == 404


def test_chat_rejects_foreign_dataset_before_calling_ai(monkeypatch):
    session = Mock()
    session.get.return_value = SimpleNamespace(
        id=42,
        user_id=200,
        analysis_result={},
    )
    monkeypatch.setattr(
        ai_routes,
        "ask_ai",
        lambda **kwargs: pytest.fail("AI provider must not be called"),
    )

    with pytest.raises(HTTPException) as error:
        ai_routes.chat(
            ai_routes.ChatRequest(message="Summarize this dataset", dataset_id=42),
            current_user=SimpleNamespace(id=100),
            session=session,
        )

    assert error.value.status_code == 403
    session.add_all.assert_not_called()


@pytest.mark.parametrize(
    "route",
    [ai_routes.chat_history, ai_routes.clear_chat_history],
)
def test_chat_history_routes_reject_foreign_dataset(route):
    session = Mock()
    session.get.return_value = SimpleNamespace(id=42, user_id=200)

    with pytest.raises(HTTPException) as error:
        route(42, current_user=SimpleNamespace(id=100), session=session)

    assert error.value.status_code == 403
    session.exec.assert_not_called()
    session.commit.assert_not_called()


def test_chat_does_not_persist_messages_when_provider_fails(monkeypatch):
    session = Mock()
    session.get.return_value = SimpleNamespace(
        id=42,
        user_id=100,
        analysis_result={},
    )
    session.exec.return_value.all.return_value = []
    monkeypatch.setattr(
        ai_routes,
        "ask_ai",
        Mock(side_effect=AIProviderError("provider request failed")),
    )

    with pytest.raises(HTTPException) as error:
        ai_routes.chat(
            ai_routes.ChatRequest(message="Summarize this dataset", dataset_id=42),
            current_user=SimpleNamespace(id=100),
            session=session,
        )

    assert error.value.status_code == 503
    assert error.value.detail == "AI service is temporarily unavailable. Please try again later."
    session.add_all.assert_not_called()
    session.commit.assert_not_called()
