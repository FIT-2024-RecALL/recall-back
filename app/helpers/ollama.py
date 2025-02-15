from ollama import AsyncClient

from app.config import _settings
from app.schemas import AIFeedback


__all__ = ["compare_answers"]


async def compare_answers(question: str, etalon: str, user: str) -> AIFeedback:
    client = AsyncClient(_settings.ollama_url)
    response = await client.generate(
        model=_settings.ollama.MODEL, stream=False, 
        prompt=f'Вопрос: {question}\nЭталонный ответ: {etalon}\nОтвет пользователя: {user}',
        format=AIFeedback.model_json_schema()
    )
    return AIFeedback.model_validate_json(response.response)
