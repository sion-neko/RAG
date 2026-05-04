from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    llm_base_url: str
    llm_model: str
    llm_api_key: str = "ollama"

    class Config:
        env_file = ".env"


settings = Settings()
