from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    # Application
    APP_NAME: str = "FastAPI Async Starter"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://app:app@localhost:5432/app"

    # Environment
    ENVIRONMENT: str = "local"

    # Server
    CORS_ORIGINS: list[str] = ["*"]
    API_V1_PREFIX: str = "/api/v1"

    # Initial admin user (created on first startup if not exists)
    SUPERUSER_EMAIL: str = "admin@example.com"
    SUPERUSER_PASSWORD: str = "admin123"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "console"  # "console" or "json"
    LOG_DIR: str = "logs"

    # Email skips sending if SMTP_HOST is empty
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "app@example.com"


settings = Settings()

SHOW_DOCS_IN = {"local", "staging"}
