from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    app_name: str = Field("Quantum-backend", alias="APP_NAME")
    debug: bool = Field(False, alias="DEBUG")

    db_host: str = Field("localhost", alias="POSTGRES_HOST")
    db_port: int = Field(5432, alias="POSTGRES_PORT")
    db_user: str = Field("user", alias="POSTGRES_USER")
    db_password: str = Field("password", alias="POSTGRES_PASSWORD")
    db_name: str = Field("database", alias="POSTGRES_DB")

    secret_key: str = Field(..., alias="SECRET_KEY")
