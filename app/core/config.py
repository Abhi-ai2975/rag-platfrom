from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "RAG Platform"
    app_env: str = "development"

    database_url: str

    qdrant_host: str = "localhost"
    qdrant_port: int = 6333

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
