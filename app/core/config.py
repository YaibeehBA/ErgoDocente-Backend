from functools import lru_cache
from typing import Literal

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Aplicación ─────────────────────────────────────────────────────────────
    APP_NAME: str = "ErgoDocente API"
    APP_VERSION: str = "1.0.0"
    APP_ENV: Literal["development", "staging", "production", "testing"] = "development"
    DEBUG: bool = True
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8080"]

    # ── API ────────────────────────────────────────────────────────────────────
    API_V1_PREFIX: str = "/api/v1"

    # ── PostgreSQL ─────────────────────────────────────────────────────────────
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "ergodocente_user"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "ergodocente_db"
    POSTGRES_SCHEMA: str = "public"

    # Pool
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    DB_POOL_TIMEOUT: int = 30
    DB_POOL_RECYCLE: int = 1800

    # ── Cloudinary ─────────────────────────────────────────────────────────────
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""
    CLOUDINARY_FOLDER_BASE: str = "ergodocente"

    # ── Seguridad / JWT (preparado para V2) ────────────────────────────────────
    SECRET_KEY: str = "cambia-esta-clave-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_RESET_EXPIRE_MINUTES: int = 15

    # ── Logging ────────────────────────────────────────────────────────────────
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    LOG_FORMAT: Literal["json", "console"] = "json"

    # ── Paginación ─────────────────────────────────────────────────────────────
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # ── Validaciones ───────────────────────────────────────────────────────────
    @field_validator("POSTGRES_PORT")
    @classmethod
    def validar_puerto(cls, v: int) -> int:
        if not (1 <= v <= 65535):
            raise ValueError("El puerto PostgreSQL debe estar entre 1 y 65535")
        return v

    @model_validator(mode="after")
    def validar_produccion(self) -> "Settings":
        if self.APP_ENV == "production":
            if self.SECRET_KEY == "cambia-esta-clave-en-produccion":
                raise ValueError("SECRET_KEY debe ser cambiada en producción")
            if self.DEBUG:
                raise ValueError("DEBUG debe ser False en producción")
        return self

    # ── URLs computadas ────────────────────────────────────────────────────────
    @property
    def database_url(self) -> str:
        """URL async para SQLAlchemy con asyncpg."""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def database_url_sync(self) -> str:
        """URL sync para Alembic con psycopg2."""
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def es_produccion(self) -> bool:
        return self.APP_ENV == "production"

    @property
    def es_testing(self) -> bool:
        return self.APP_ENV == "testing"

    @property
    def cloudinary_configurado(self) -> bool:
        return all([
            self.CLOUDINARY_CLOUD_NAME,
            self.CLOUDINARY_API_KEY,
            self.CLOUDINARY_API_SECRET,
        ])


@lru_cache
def get_settings() -> Settings:
    """
    Retorna la instancia singleton de Settings.
    Usar @lru_cache evita releer el .env en cada request.
    """
    return Settings()


settings: Settings = get_settings()