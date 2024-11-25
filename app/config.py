from enum import StrEnum

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class CryptoAlgorithm(StrEnum):
    HS256 = "HS256"
    HS512 = "HS512"


class SameSiteEnum(StrEnum):
    LAX = 'lax'
    STRICT = 'strict'
    NONE = 'none'


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./config/auth.env")

    SECRET_KEY: SecretStr
    ALGORITHM: CryptoAlgorithm = CryptoAlgorithm.HS256

    ACCESS_TOKEN_KEY: str
    HTTPONLY: bool = True
    SECURE: bool = True
    SAMESITE: SameSiteEnum = SameSiteEnum.NONE


class PostgreSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='POSTGRES_', env_file="./config/postgres.env")

    USER: str
    PASSWORD: SecretStr
    HOST: str
    HOST_PORT: int
    DB_NAME: str


class Settings(BaseSettings):
    auth: AuthSettings = AuthSettings()
    db: PostgreSettings = PostgreSettings()

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
    def cookie_kwargs(self) -> dict:
        return {
            'httponly': self.auth.HTTPONLY,
            'secure': self.auth.SECURE,
            'samesite': self.auth.SAMESITE
        }

    def __create_dialect_url(self, dialect: str) -> str:
        return (f"postgresql+{dialect}://{self.db.USER}:{self.db.PASSWORD.get_secret_value()}"
                f"@{self.db.HOST}:{self.db.HOST_PORT}/{self.db.DB_NAME}")

    @property
    def db_url_asyncpg(self) -> str:
        return self.__create_dialect_url("asyncpg")

    @property
    def db_url_psycopg(self) -> str:
        return self.__create_dialect_url("psycopg")

    @property
    def db_url_pysqlite(self) -> str:
        return "sqlite:///./sql_app.db"


_settings = Settings()
