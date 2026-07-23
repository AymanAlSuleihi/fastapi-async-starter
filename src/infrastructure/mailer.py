"""SMTP mailer. Logs and skips if unconfigured — safe for local dev."""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.core.config import settings
from src.extensions.logs import get_logger

logger = get_logger(__name__)


class Mailer:
    def send(self, *, to: str, subject: str, body: str, html: bool = False) -> None:
        if not settings.SMTP_HOST:
            logger.info("email_skipped", to=to, subject=subject, reason="SMTP not configured")
            return

        msg = MIMEMultipart()
        msg["From"] = settings.EMAIL_FROM
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html" if html else "plain"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
            if settings.SMTP_USER:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        logger.info("email_sent", to=to, subject=subject)
