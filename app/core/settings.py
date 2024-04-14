from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Meduzzen Internship Project"
    host: str
    port: int
    db_name: str
    db_username: str
    db_password: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
