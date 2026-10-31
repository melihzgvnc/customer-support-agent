from pathlib import Path
from functools import lru_cache
from typing import Literal
from pydantic import SecretStr, HttpUrl, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_file_secrets import FileSecretsSettingsSource

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class LLMSettings(BaseModel):
    openrouter_api_key: SecretStr
    openrouter_base_url: HttpUrl
    openai_api_key: SecretStr

class WebhookSettings(BaseModel):
    zendesk_subdomain: str
    zendesk_client_id: str
    zendesk_client_secret: SecretStr

class DBSettings(BaseModel):
    postgres_user: str
    postgres_db: str
    postgres_password: SecretStr
    garage_rpc_secret: SecretStr
    garage_admin_token: SecretStr
    s3_endpoint_url: HttpUrl
    s3_region: str
    s3_bucket: str
    s3_access_key_id: str
    s3_secret_access_key: str

class MonitorSettings(BaseModel):
    langsmith_api_key: SecretStr

class Settings(BaseSettings):
    environment: Literal["dev", "staging", "prod"] = "dev"
    data_dir: Path = PROJECT_ROOT/"data"

    llm: LLMSettings
    webhook: WebhookSettings
    monitor: MonitorSettings
    db: DBSettings

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
        # secrets_dir="/run/secrets",
        secrets_dir=Path(__file__).resolve().parents[2]/"secrets",
        secrets_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore"
    )

    @classmethod
    def settings_customise_sources(
        cls, settings_cls, init_settings, env_settings,
        dotenv_settings, file_secret_settings,
    ):
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            FileSecretsSettingsSource(file_secret_settings),
        )

@lru_cache
def get_settings() -> Settings:
    return Settings()

