from unittest.mock import MagicMock, patch

from src.core.config import settings
from src.services.mailer import Mailer


class TestMailer:
    def test_send_skips_when_smtp_not_configured(self):
        """When SMTP_HOST is empty, send() logs and returns without connecting."""
        mailer = Mailer()
        # Default settings.SMTP_HOST is ""; no SMTP call should happen
        with patch("src.services.mailer.logger") as mock_logger:
            mailer.send(to="test@example.com", subject="Hello", body="World")
            mock_logger.info.assert_called_once_with(
                "email_skipped",
                to="test@example.com",
                subject="Hello",
                reason="SMTP not configured",
            )

    def test_send_connects_and_sends_when_configured(self):
        """When SMTP_HOST is set, send() connects and sends the email."""
        mailer = Mailer()

        with patch("src.services.mailer.smtplib.SMTP") as mock_smtp_class:
            mock_server = MagicMock()
            mock_smtp_class.return_value.__enter__.return_value = mock_server

            with (
                patch.object(settings, "SMTP_HOST", "smtp.example.com"),
                patch.object(settings, "SMTP_USER", "user"),
                patch.object(settings, "SMTP_PASSWORD", "pass"),
            ):
                mailer.send(
                    to="test@example.com",
                    subject="Hello",
                    body="<p>World</p>",
                    html=True,
                )

            mock_smtp_class.assert_called_once_with("smtp.example.com", 587, timeout=10)
            mock_server.starttls.assert_called_once()
            mock_server.login.assert_called_once_with("user", "pass")
            mock_server.send_message.assert_called_once()
            # Verify the message is HTML
            msg = mock_server.send_message.call_args[0][0]
            assert msg["From"] == settings.EMAIL_FROM
            assert msg["To"] == "test@example.com"
            assert msg["Subject"] == "Hello"

    def test_send_without_auth(self):
        """When SMTP_USER is empty, no auth/starttls is performed."""
        mailer = Mailer()

        with patch("src.services.mailer.smtplib.SMTP") as mock_smtp_class:
            mock_server = MagicMock()
            mock_smtp_class.return_value.__enter__.return_value = mock_server

            with (
                patch.object(settings, "SMTP_HOST", "smtp.example.com"),
                patch.object(settings, "SMTP_USER", ""),
            ):
                mailer.send(to="test@example.com", subject="Hello", body="World")

            mock_smtp_class.assert_called_once()
            mock_server.starttls.assert_not_called()
            mock_server.login.assert_not_called()
            mock_server.send_message.assert_called_once()
