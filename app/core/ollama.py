from ollama import AsyncClient, ShowResponse

from app.schemas import AIFeedback

from .config import get_settings


__all__ = ["load_model", "unload_model", "compare_answers"]


client = AsyncClient(get_settings().ollama_url)


async def load_model():
    return await client.generate(get_settings().ollama.MODEL, keep_alive=-1)


async def unload_model():
    return await client.generate(get_settings().ollama.MODEL, keep_alive=0)


async def compare_answers(question: str, etalon: str, user: str) -> AIFeedback:
    response = await client.generate(
        model=get_settings().ollama.MODEL, keep_alive=-1,
        prompt=f'Вопрос: {question}\nЭталонный ответ: {etalon}\nОтвет пользователя: {user}',
        format=AIFeedback.model_json_schema()
    )
    return AIFeedback.model_validate_json(response.response)
