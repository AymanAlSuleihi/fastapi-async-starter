import pytest

from src.auth.config import auth_settings
from src.auth.exceptions import InvalidCredentials, InvalidResetToken
from src.auth.utils import (
    create_access_token,
    create_refresh_token,
    create_reset_token,
    decode_token,
    hash_password,
    verify_password,
    verify_reset_token,
)


class TestPasswordUtils:
    def test_hash_and_verify(self):
        password = "securepassword123"
        hashed = hash_password(password)
        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("wrong", hashed) is False


class TestTokenUtils:
    def test_create_and_decode_access_token(self):
        data = {"sub": "user-123"}
        token = create_access_token(data)
        decoded = decode_token(token)
        assert decoded["sub"] == "user-123"

    def test_create_and_decode_refresh_token(self):
        data = {"sub": "user-123"}
        token = create_refresh_token(data)
        decoded = decode_token(token, secret=auth_settings.REFRESH_TOKEN_KEY)
        assert decoded["sub"] == "user-123"

    def test_decode_invalid_token(self):
        with pytest.raises(InvalidCredentials):
            decode_token("invalid.token.here")

    def test_access_token_contains_expiry(self):
        token = create_access_token({"sub": "test"})
        decoded = decode_token(token)
        assert "exp" in decoded


class TestResetTokenUtils:
    def test_create_and_verify_reset_token(self):
        token = create_reset_token("user-456")
        payload = verify_reset_token(token)
        assert payload["sub"] == "user-456"
        assert payload["type"] == "password_reset"

    def test_verify_invalid_reset_token(self):
        with pytest.raises(InvalidResetToken):
            verify_reset_token("invalid.token.here")

    def test_verify_access_token_as_reset_fails(self):
        access_token = create_access_token({"sub": "user-123"})
        with pytest.raises(InvalidResetToken):
            verify_reset_token(access_token)
