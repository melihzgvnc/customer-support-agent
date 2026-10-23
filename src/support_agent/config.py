from pathlib import Path
from functools import lru_cache
from typing import Literal
from pydantic import SecretStr, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class LLMSettings(BaseSettings):
    openrouter_api_key: SecretStr
    openrouter_base_url: HttpUrl
    openai_api_key: SecretStr
    langsmith_api_key: SecretStr | None

class WebhookSettings(BaseSettings):
    zendesk_subdomain: str
    zendesk_client_id: str
    zendesk_client_secret: SecretStr

class MonitorSettings(BaseSettings):
    langsmith_api_key: SecretStr

class Settings(BaseSettings):
    environment: Literal["dev", "staging", "prod"] = "dev"
    data_dir: Path = PROJECT_ROOT/"data"

    llm: LLMSettings
    webhook: WebhookSettings
    monitor: MonitorSettings

    @property
    def dense_index_path(self) -> Path:
        return self.data_dir/"index"/"dense"

    @property
    def sparse_index_path(self) -> Path:
        return self.data_dir/"index"/"sparse"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2]/".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore"
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()