from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./config/backend.env", extra="allow")

    SECRET_KEY: str
    ALGORITHM: str

    @property
    def get_auth_data(self) -> dict[str, str]:
        return {"secret_key": self.SECRET_KEY, "algorithm": self.ALGORITHM}


authSettings: AuthSettings = AuthSettings()
