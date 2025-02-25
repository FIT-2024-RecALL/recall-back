# Ollama setupn container
Connects to ollama's server and creates model with special [system prompt](./system_prompt.md)

Next env variables should be specified for container:
```conf
FROM_MODEL: "llama3.1" | "mistral"
MODEL: str
HOSTNAME: str
PORT: int
```