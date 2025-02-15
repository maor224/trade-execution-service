from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ALPACA_API_KEY: str
    ALPACA_SECRET_KEY: str
    ALPACA_BASE_URL: str

    class Config:
        env_file = ".env"

_settings = None

def get_settings():
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
