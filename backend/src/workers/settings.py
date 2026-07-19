from pydantic_settings import BaseSettings, SettingsConfigDict
from taskiq_valkey import ValkeyStreamBroker


class WorkerConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="VALKEY_")
    VALKEY_HOST: str = "valkey"
    VALKEY_PORT: int = 6379
    VALKEY_DB: int = 0


worker_config = WorkerConfig()

valkey_url = (
    f"valkey://{worker_config.VALKEY_HOST}:{worker_config.VALKEY_PORT}/{worker_config.VALKEY_DB}"
)

broker = ValkeyStreamBroker(valkey_url)
import src.workers.tasks  # noqa: F401, E402
