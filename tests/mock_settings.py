from pydantic_settings import BaseSettings

class MockSettings(BaseSettings):
    ALPACA_API_KEY: str = "test_api_key"
    ALPACA_SECRET_KEY: str = "test_secret_key"
    ALPACA_BASE_URL: str = "https://paper-api.alpaca.markets"
    
    class Config:
        env_file = None