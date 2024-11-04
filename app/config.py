from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_DB_USER: str
    POSTGRES_DB_PASSWORD: str
    POSTGRES_DB_HOST: str
    POSTGRES_DB_HOST_PORT: int
    POSTGRES_DB_NAME: str

    @staticmethod
    def __create_dialect_url(self, dialect: str) -> str:
        return (f"postgresql+{dialect}://{self.POSTGRES_DB_USER}:{self.POSTGRES_DB_PASSWORD}"
                f"@{self.POSTGRES_DB_HOST}:{self.POSTGRES_DB_HOST_PORT}/{self.POSTGRES_DB_NAME}")

    @property
    def db_url_asyncpg(self) -> str:
        return Settings.__create_dialect_url(self, "asyncpg")

    @property
    def db_url_psycopg(self) -> str:
        return Settings.__create_dialect_url(self, "psycopg")

    @property
    def db_url_pysqlite(self) -> str:
        return "sqlite:///./sql_app.db"

    model_config = SettingsConfigDict(env_file=".env")

dbSettings = Settings()
