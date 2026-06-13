from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    HTTP_TIMEOUT: float = 3.0
    HTTP_RETRIES: int = 2
    PARALLEL_URLS: int = 10
    TARGET_URL: str = "https://jsonplaceholder.typicode.com/todos/1"

settings = Settings()