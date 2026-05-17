from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Dashboard Backend"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/business_dashboard"
    secret_key: str = "change-me-to-a-long-random-string"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    admin_email: str = "admin@example.com"
    admin_password: str = "admin12345"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)


settings = Settings()
