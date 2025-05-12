from enum import StrEnum
from functools import cache
from pydantic import SecretStr, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ["get_settings", "Settings"]


class CryptoAlgorithm(StrEnum):
    HS256 = "HS256"
    HS512 = "HS512"


class SameSiteEnum(StrEnum):
    LAX = 'lax'
    STRICT = 'strict'
    NONE = 'none'


class CookieSettings(BaseModel):
    httponly: bool
    secure: bool
    samesite: SameSiteEnum


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./config/auth.env", extra="ignore")

    SECRET_KEY: SecretStr
    ALGORITHM: CryptoAlgorithm = CryptoAlgorithm.HS256

    ACCESS_TOKEN_KEY: str
    EXPIRE_HOURS: int = 12
    HTTPONLY: bool = True
    SECURE: bool = False
    SAMESITE: SameSiteEnum = SameSiteEnum.LAX


class PostgreSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='POSTGRES_', env_file="./config/postgres.env", extra="ignore")

    USER: str
    PASSWORD: SecretStr
    HOST: str
    HOST_PORT: int
    DB: str


class MinioSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='MINIO_', env_file="./config/minio-backend.env", extra="ignore")

    BUCKET_NAME: str
    HOSTNAME: str
    PORT: int
    LOGIN: str
    PASSWORD: str


class OllamaSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='OLLAMA_', env_file="./config/ollama.env", extra="ignore")

    MODEL: str
    HOSTNAME: str
    PORT: int


class Settings(BaseSettings):
    auth: AuthSettings = AuthSettings()
    db: PostgreSettings = PostgreSettings()
    minio: MinioSettings = MinioSettings()
    ollama: OllamaSettings = OllamaSettings()

    @staticmethod
    @cache
    def get_api_hosts() -> list[str]:
        return ['https://letsrecall.ru/api', 'http://letsrecall.ru/api', 'http://localhost:8000']

    @property
    def auth_algorithm(self) -> CryptoAlgorithm:
        return self.auth.ALGORITHM

    @property
    def auth_secret_key(self) -> SecretStr:
        return self.auth.SECRET_KEY
    
    @property
    def access_token_key(self) -> str:
        return self.auth.ACCESS_TOKEN_KEY
    
    @property
    def expire_hours(self) -> int:
        return self.auth.EXPIRE_HOURS

    @property
    @cache
    def cookie_kwargs(self) -> CookieSettings:
        return CookieSettings(
            httponly=self.auth.HTTPONLY, secure=self.auth.SECURE, samesite=self.auth.SAMESITE
        )

    @property
    @cache
    def minio_url(self) -> str:
        """Hostname with port"""
        return f"{self.minio.HOSTNAME}:{self.minio.PORT}"

    @property
    @cache
    def ollama_url(self) -> str:
        return f"http://{self.ollama.HOSTNAME}:{self.ollama.PORT}"

    @cache
    def __create_postgres_dialect_url(self, dialect: str) -> str:
        return (f"postgresql+{dialect}://{self.db.USER}:{self.db.PASSWORD.get_secret_value()}"
                f"@{self.db.HOST}:{self.db.HOST_PORT}/{self.db.DB}")

    @property
    def db_url_asyncpg(self) -> str:
        return self.__create_postgres_dialect_url("asyncpg")

    @property
    def db_url_psycopg(self) -> str:
        return self.__create_dialect_url("psycopg")

    @property
    def db_url_pysqlite(self) -> str:
        return "sqlite:///./sql_app.db"


__settings = Settings()


@cache
def get_settings() -> Settings:
    return __settings
