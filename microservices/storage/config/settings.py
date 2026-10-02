from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración centralizada del Storage (12-factor: config desde entorno)."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    app_name: str = "extracText Storage"
    app_version: str = "0.1.0"
    app_debug: bool = False

    mongodb_url: str = "mongodb://mongo:27017"
    mongodb_db_name: str = "extractext"


settings = Settings()
