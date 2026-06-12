from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    EXTERNAL_API_URL: str = "https://jsonexampletest.com/api/v1"
    HTTP_TIMEOUT: float = 2.0
    HTTP_RETRIES: int = 3
    CIRCUIT_FAIL_THRESHOLD: int = 5
    CIRCUIT_RESET_TIMEOUT: int = 30


settings = Settings()

