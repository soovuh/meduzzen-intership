from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Meduzzen Internship Project"
    host: str
    port: str

    model_config = SettingsConfigDict(env_file=".env")
