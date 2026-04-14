from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    APP_ENV: str = "development"

    # PostgreSQL
    DATABASE_URL: str = "postgresql+asyncpg://middleware:middleware@localhost:5432/middleware"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    SESSION_TTL_SECONDS: int = 1800

    # GLPI
    GLPI_URL: str = "https://glpi.example.com/apirest.php"
    GLPI_APP_TOKEN: str = ""
    GLPI_USER_TOKEN: str = ""

    # Evolution API
    EVOLUTION_URL: str = "http://localhost:8080"
    EVOLUTION_API_KEY: str = ""
    EVOLUTION_INSTANCE: str = ""


def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
