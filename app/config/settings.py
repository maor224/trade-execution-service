from pydantic import BaseSettings

class Settings(BaseSettings):
    ALPACA_API_KEY: str
    ALPACA_SECRET_KEY: str
    ALPACA_BASE_URL: str

    class Config:
        env_file = ".env"  # Specify the environment file

settings = Settings()
