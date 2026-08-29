from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central app configuration, overridable via environment variables or a .env file."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Image Quality & Defect Detection API"
    environment: str = "development"

    # Where uploaded images and the SQLite file live
    database_url: str = "sqlite:///./data/app.db"
    upload_dir: str = "./data/uploads"

    # Frontend origin, for CORS during local dev
    frontend_origin: str = "http://localhost:5173"

    max_upload_size_mb: int = 10


settings = Settings()
