from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración centralizada de la aplicación (12-factor: config desde entorno)."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    app_name: str = "extracText"
    app_version: str = "0.1.0"
    app_debug: bool = False

    mongodb_url: str = "mongodb://localhost:27017"
    mongodb_db_name: str = "extractext"

    pdf_max_size_mb: int = 10

    @property
    def pdf_max_size_bytes(self) -> int:
        return self.pdf_max_size_mb * 1024 * 1024


settings = Settings()
