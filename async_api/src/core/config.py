from logging import config as logging_config
from typing import Any
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel

from . import logger


# Применяем настройки логированияs
logging_config.dictConfig(logger.LOGGING)

BASE_DIR = Path(__file__).parent.parent.parent


class AuthJWT(BaseModel):
    public_key_path: Path = BASE_DIR / 'certs' / 'public.pem'
    algorithm: str = 'RS256'


class Settings(BaseSettings):
    # Название проекта. Используется в Swagger-документации
    project_name: str = "Async API"

    # Настройки Uvicorn
    uvicorn_host: str
    uvicorn_port: int

    # Настройки Redis
    redis_host: str
    redis_port: int

    # Настройки Elasticsearch
    elastic_host: str
    elastic_port: int

    # Настройки JWT при авторизации
    jwt_settings: AuthJWT = AuthJWT()

    # Настройки kafka
    bootstrap_servers: str

    #model_config = SettingsConfigDict(env_file=f'{BASE_DIR} / src /.env')


settings = Settings()
