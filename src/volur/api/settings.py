from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class VolurApiSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="VOLUR_API_",
    )
    address: str
    token: SecretStr
    debug: bool = Field(False, description="Enable debug mode")
