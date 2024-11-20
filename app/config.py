from enum import StrEnum

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class CryptoAlgorithm(StrEnum):
    HS256 = "HS256"
    HS512 = "HS512"


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./config/auth.env")

    SECRET_KEY: SecretStr
    ALGORITHM: CryptoAlgorithm = CryptoAlgorithm.HS256


class PostgreSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='POSTGRES_', env_file="./config/postgres.env")

    USER: str
    PASSWORD: str
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

    def __create_dialect_url(self, dialect: str) -> str:
        return (f"postgresql+{dialect}://{self.db.USER}:{self.db.PASSWORD}"
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


settings: Settings = Settings()
