from ollama import Client

from .settings import OllamaSetupSettings

settings = OllamaSetupSettings()
client = Client(settings.ollama_url)

with open('./system_prompt.md', 'r', encoding='utf-8') as system_prompt_file:
    system_prompt = system_prompt_file.read()
    create_response = client.create(
        settings.MODEL,
        from_=settings.FROM_MODEL,
        system=system_prompt
    )
    print(create_response.status)
