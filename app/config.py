from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgreSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='POSTGRES_', env_file="/../config/postgres.env")

    USER: str
    PASSWORD: str
    HOST: str
    HOST_PORT: int
    DB_NAME: str

    @staticmethod
    def __create_dialect_url(self, dialect: str) -> str:
        return (f"postgresql+{dialect}://{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_HOST_PORT}/{self.DB_NAME}")

    @property
    def db_url_asyncpg(self) -> str:
        return PostgreSettings.__create_dialect_url(self, "asyncpg")

    @property
    def db_url_psycopg(self) -> str:
        return PostgreSettings.__create_dialect_url(self, "psycopg")

    @property
    def db_url_pysqlite(self) -> str:
        return "sqlite:///./sql_app.db"


dbSettings: PostgreSettings = PostgreSettings()
