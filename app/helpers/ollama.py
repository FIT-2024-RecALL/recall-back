from ollama import AsyncClient, ShowResponse

from app.config import _settings
from app.schemas import AIFeedback


__all__ = ["load_model", "unload_model", "compare_answers"]


client = AsyncClient(_settings.ollama_url)


async def load_model():
    return await client.generate(_settings.ollama.MODEL, keep_alive=-1)


async def unload_model():
    return await client.generate(_settings.ollama.MODEL, keep_alive=0)


async def compare_answers(question: str, etalon: str, user: str) -> AIFeedback:
    response = await client.generate(
        model=_settings.ollama.MODEL, keep_alive=-1,
        prompt=f'Вопрос: {question}\nЭталонный ответ: {etalon}\nОтвет пользователя: {user}',
        format=AIFeedback.model_json_schema()
    )
    return AIFeedback.model_validate_json(response.response)
