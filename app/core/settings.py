from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Meduzzen Internship Project"
    host: str
    port: int
    db_host: str
    db_name: str
    db_username: str
    db_password: str
    redis_host: str
    redis_port: int

    jwt_secret_key: str
    jwt_refresh_secret_key: str
    jwt_algorhitm: str

    auth0_domain: str
    auth0_api_audience: str
    auth0_issuer: str
    auth0_algorhitm: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
