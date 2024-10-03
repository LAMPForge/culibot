from enum import StrEnum
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn
from typing import Literal

class Environment(StrEnum):
    development = "development"
    production = "production"


class EmailSender(StrEnum):
    logger = "logger"
    resend = "resend"


env = Environment(os.getenv("CULI_ENV", Environment.development))
env_file = ".env"


class Settings(BaseSettings):
    ENV: Environment = Environment.development
    DEBUG: bool = False
    LOG_LEVEL: str = "DEBUG"

    SECRET: str = "super secret jwt secret"

    # JSON list of accepted CORS origins
    CORS_ORIGINS: list[str] = []

    ALLOWED_HOSTS: set[str] = {"127.0.0.1:3000", "localhost:3000"}

    # Auth cookie
    AUTH_COOKIE_KEY: str = "polar_session"
    AUTH_COOKIE_TTL_SECONDS: int = 60 * 60 * 24 * 31  # 31 days
    AUTH_COOKIE_DOMAIN: str = "127.0.0.1"

    # Auth Link
    AUTH_LINK_TTL_SECONDS: int = 60 * 60  # 1 hour

    # Emails
    EMAIL_SENDER: EmailSender = EmailSender.logger
    RESEND_API_KEY: str = ""
    EMAIL_FROM_NAME: str = "Polar"
    EMAIL_FROM_EMAIL_ADDRESS: str = "culi@lampforge.com"

    BASE_URL: str = "http://127.0.0.1:8000/v1"
    FRONTEND_BASE_URL: str = "http://127.0.0.1:3000"
    FRONTEND_DEFAULT_RETURN_PATH: str = "/"

    # Database
    POSTGRES_USER: str = "postgres"
    POSTGRES_PWD: str = "root"
    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: int = 5432
    POSTGRES_DATABASE: str = "culi"
    DATABASE_POOL_SIZE: int = 5
    DATABASE_SYNC_POOL_SIZE: int = 1  # Specific pool size for sync connection: since we only use it in OAuth2 router, don't waste resources.
    DATABASE_POOL_RECYCLE_SECONDS: int = 600  # 10 minutes

    model_config = SettingsConfigDict(
        env_prefix="polar_",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_file=env_file,
        extra="allow",
    )

    def get_postgres_dsn(self, driver: Literal["asyncpg", "psycopg2"]) -> str:
        return str(
            PostgresDsn.build(
                scheme=f"postgresql+{driver}",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PWD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DATABASE,
            )
        )

    def is_environment(self, environments: set[Environment]) -> bool:
        return self.ENV in environments

    def is_development(self) -> bool:
        return self.is_environment({Environment.development})

    def is_production(self) -> bool:
        return self.is_environment({Environment.production})

    def generate_external_url(self, path: str) -> str:
        return f"{self.BASE_URL}{path}"

    def generate_frontend_url(self, path: str) -> str:
        return f"{self.FRONTEND_BASE_URL}{path}"


settings = Settings()
