from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

    pg_dbname: str = Field(..., alias='POSTGRES_DB')
    pg_user: str = Field(..., alias='POSTGRES_USER')
    pg_password: str = Field(..., alias='POSTGRES_PASSWORD')
    pg_host: str = Field(..., alias='POSTGRES_HOST')
    pg_port: int = Field(..., alias='POSTGRES_PORT')

    initial_date: str = '2021-01-01'
    delay: int = 3600



