from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

    # PostgreSQL settings
    postgres_dbname: str = Field(..., alias='POSTGRES_DB')
    postgres_user: str = Field(..., alias='POSTGRES_USER')
    postgres_password: str = Field(..., alias='POSTGRES_PASSWORD')
    postgres_host: str = Field(..., alias='POSTGRES_HOST')
    postgres_port: int = Field(..., alias='POSTGRES_PORT')

    # Elasticsearch settings
    elastic_host: str = Field(..., alias='ELASTIC_HOST')
    elastic_port: int = Field(..., alias='ELASTIC_PORT')
    elastic_index_name: str = Field(default="movies", alias='ELASTIC_INDEX_NAME')

    # General app settings
    initial_date: str = Field(default='2021-01-01', alias='INITIAL_DATE')
    delay: int = Field(default=3600, alias='DELAY')
