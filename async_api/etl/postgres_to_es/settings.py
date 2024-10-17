from pydantic_settings import BaseSettings, SettingsConfigDict


# BASE_DIR = Path(__file__).parent.parent.parent
# ENV_FILE_PATH = BASE_DIR / '.env'

# BASE_DIR = Path(__file__).parent.parent.parent
ENV_FILE_PATH = 'postgres_to_es/.env'


class Settings(BaseSettings):
    # PostgreSQL
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str

    # Elasticsearch
    elasticsearch_host: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH, env_file_encoding='utf-8'
    )


settings = Settings()

# Определить Data Source Name для подключения к базе данных (БД)
DSN = {
    'dbname': settings.postgres_db,
    'user': settings.postgres_user,
    'password': settings.postgres_password,
    'host': settings.postgres_host,
    'port': settings.postgres_port,
}

# Настройки для процесса извлечения данных из БД

# Определить название файла в формате json для сохранения состояний системы
FILE_PATH = 'postgres_to_es/state_storage.json'

# Определить названия подхранилищ для имеющихся таблиц: film_work, person,
# genre. Состояние будет сохраняться для каждого подхранилища при работе
# с соответствующей таблицей
FILM_WORKS_SUBSTORAGE = 'film_works'
PERSONS_SUBSTORAGE = 'persons'
GENRES_SUBSTORAGE = 'genres'
SUBSTORAGES = [FILM_WORKS_SUBSTORAGE, PERSONS_SUBSTORAGE, GENRES_SUBSTORAGE]

# Настройки для процесса загрузки данных в Elasticsearch (ES)

# Определить время, с которого необходимо определять обновленные записи
# в таблицах, и ограничение количества выгружаемых записей
MODIFIED_TIME = '2020-01-01'
ROW_LIMIT = 200

# Определить путь к файлу, содержащему схему данных индекса ES
FILE_PATH_TO_ES_SCHEMA = 'postgres_to_es/es_schema.json'

# Определить наименование индекса в ES
MOVIES_INDEX_NAME = 'movies'
GENRES_INDEX_NAME = 'genres'
PERSONS_INDEX_NAME = 'persons'

# Определить время, через которое планировщик задач будет
# запускать ETL-процесс, сек.
SCHEDULER_TIME_INTERVAL = 30
