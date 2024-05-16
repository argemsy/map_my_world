# Third-party Libraries
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    COMPOSE_PROJECT_NAME: str = Field(
        env="COMPOSE_PROJECT_NAME",
        default="map_my_world",
    )
    DJANGO_SETTINGS_MODULE: str = Field(
        env="DJANGO_SETTINGS_MODULE",
        default="config.settings.base",
    )
    SECRET_KEY: SecretStr | None = Field(
        default="*",
        env="SECRET_KEY",
    )
    DEBUG: bool = Field(env="DEBUG", default=True)
    JWT_SECRET_KEY: SecretStr | None = Field(
        default="insecure-jwt-secret-key",
        env="JWT_SECRET_KEY",
    )
    SITE_URL: str = Field(env="SITE_URL", default="http://localhost:8500")
    DATABASE_URL: str | None = Field(
        default="postgresql://postgres:postgres@postgres:5432/postgres",
        env="DATABASE_URL",
    )
    DJANGO_ALLOW_ASYNC_UNSAFE: bool = Field(
        default=True,
        env="DJANGO_ALLOW_ASYNC_UNSAFE",
    )


settings = Settings()
