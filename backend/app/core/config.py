from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    database_url: str = "sqlite:///./debate_arena.db"
    model_checkpoint: str = "distilbert-base-uncased"
    scorer_model_path: str = "./trained_scorer"
    debug: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
