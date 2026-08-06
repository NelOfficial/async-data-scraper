from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_PATH: str = "parser.db"
    MAX_CONCURRENT_REQUESTS: int = 5
    TIMEOUT_SECONDS: int = 10

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()