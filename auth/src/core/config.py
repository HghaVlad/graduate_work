from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


BASE_DIR = Path(__file__).parent.parent.parent
ENV_FILE_PATH = BASE_DIR / '.env'


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / 'certs' / 'private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'public.pem'
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60


class ServiceSettings(BaseSettings):
    # Database settings
    postgres_user: str
    postgres_db: str
    postgres_password: str
    postgres_host: str
    postgres_port: str

    # Database engine settings
    db_echo: bool

    # Redis settings
    redis_host: str
    redis_port: int

    # RabbitMQ settings
    rabbitmq_host: str
    rabbitmq_port: int
    rabbitmq_username: str
    rabbitmq_password: str

    # Jaeger settings
    jaeger_host: str
    jaeger_port: int
    jaeger_console_output: bool = False
    jaeger_configure_tracer: bool = False  # Set to True to allow Jaeger tracing
    otel_resource_attributes: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH, env_file_encoding='utf-8'
    )


class OAuthSettings(BaseSettings):
    oauth_provider: str = 'google'
    oauth_client_id: str = '1065143737604-mqo6qe5rhq167ivoe8bi90nupmhavrv5.apps.googleusercontent.com'
    oauth_client_secret: str = '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'
    # authorization_url: str = ...
    oauth_google_server_metadata_url: str = 'https://accounts.google.com/.well-known/openid-configuration'


class Settings(BaseSettings):
    service_settings: ServiceSettings = ServiceSettings()
    jwt_settings: AuthJWT = AuthJWT()

    REQUEST_LIMIT_PER_MINUTE: int = 20

    oauth_settings: OAuthSettings = OAuthSettings()

    db_url: str = (
        f'postgresql+asyncpg://{service_settings.postgres_user}'
        f':{service_settings.postgres_password}@{service_settings.postgres_host}'
        f':{service_settings.postgres_port}/{service_settings.postgres_db}'
    )


settings = Settings()
