from pydantic import ValidationError
import pytest

from backend.schemas.auth_schema import LoginSchema, RegisterSchema


def test_register_schema_normalizes_name():
    payload = RegisterSchema(
        name="  Harsh  ",
        email="harsh@example.com",
        password="strong-password",
    )
    assert payload.name == "Harsh"
    assert str(payload.email) == "harsh@example.com"


def test_register_schema_rejects_short_password():
    with pytest.raises(ValidationError):
        RegisterSchema(
            name="Harsh",
            email="harsh@example.com",
            password="short",
        )


def test_login_schema_validates_email():
    with pytest.raises(ValidationError):
        LoginSchema(email="not-an-email", password="password")
