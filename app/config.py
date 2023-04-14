from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Code Evaluation Sandbox API"
    API_V1_STR: str = "/api/v1"
    DEFAULT_TIMEOUT_SECONDS: float = 5.0
    MAX_TIMEOUT_SECONDS: float = 15.0
    MAX_CODE_SIZE_BYTES: int = 65536  # 64 KB

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")


settings = Settings()
