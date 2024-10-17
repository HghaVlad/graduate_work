from pydantic import Field
from pydantic_settings import BaseSettings

from src.tests.functional.testdata.es_mappings import es_movie_mappings, \
    es_person_mappings, es_genre_mappings
from src.tests.functional.testdata.es_settings import es_movie_settings, \
    es_person_settings, es_genre_settings


class TestSettings(BaseSettings):
    es_host: str = Field(
        default='elasticsearch',
        json_schema_extra={'env': 'ELASTIC_HOST'}
    )
    es_port: int = Field(
        default=9200,
        json_schema_extra={'env': 'ELASTIC_PORT'}
    )

    redis_host: str = Field(
        default='redis',
        json_schema_extra={'env': 'REDIS_HOST'}
    )
    redis_port: int = Field(
        default=6379,
        json_schema_extra={'env': 'REDIS_PORT'}
    )

    service_url: str = Field(
        default='http://127.0.0.1:8000/',
        json_schema_extra={'env': 'SERVICE_URL'}
    )


class MovieTestSettings(TestSettings):
    es_index: str = Field(
        default='movies',
        json_schema_extra={'env': 'ELASTIC_MOVIES_INDEX'}
    )
    es_index_mappings: dict = Field(default=es_movie_mappings)
    es_index_settings: dict = Field(default=es_movie_settings)


class PersonTestSettings(TestSettings):
    es_index: str = Field(
        default='persons',
        json_schema_extra={'env': 'ELASTIC_PERSONS_INDEX'}
    )
    es_index_mappings: dict = Field(default=es_person_mappings)
    es_index_settings: dict = Field(default=es_person_settings)


class GenreTestSettings(TestSettings):
    es_index: str = Field(
        default='genres',
        json_schema_extra={'env': 'ELASTIC_GENRES_INDEX'}
    )
    es_index_mappings: dict = Field(default=es_genre_mappings)
    es_index_settings: dict = Field(default=es_genre_settings)


test_settings = TestSettings()
movie_test_settings = MovieTestSettings()
person_test_settings = PersonTestSettings()
genre_test_settings = GenreTestSettings()
