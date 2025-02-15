from enum import StrEnum

from pydantic_settings import BaseSettings, SettingsConfigDict

class FromModelEnum(StrEnum):
    LLAMA31 = "llama3.1"
    MISTRAL = "mistral"


class OllamaSetupSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='OLLAMA_', extra="ignore")
    
    FROM_MODEL: FromModelEnum = FromModelEnum.LLAMA31

    MODEL: str
    HOSTNAME: str
    PORT: int

    @property
    def ollama_url(self) -> str:
        return f'http://{self.HOSTNAME}:{self.PORT}'