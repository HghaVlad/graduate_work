# Проектная работа 7 спринта

### Над спринтом работали:
- Тараканов Денис - тимлид; разработка API для сайта и личного кабинета;
- Ивахин Дмитрий - разработчик; разработка API для управления ролями
(https://github.com/DSIvahin/Auth_sprint_1)

### URL проекта для проверки:
- https://github.com/tarakanovdenis/Auth_sprint_2

### Перед разворачиванием и запуском сервисов необходимо сделать следующее:
- Перенести переменные окружения из .env.example в .env в следующих директориях (.env и сертификаты для проверки подписи токенов намеренно не добавлены в .gitignore, чтобы не тратить время для настройки переменных окружения):
    - `./admin_panel/django_api/` (admin panel service)
    - `./async_api/src/` (async api service)
    - `./async_api/etl/` и `./async_api/postgres_to_es/` (etl service)
    - `./async_api/` (elasticsearch)
    - `./auth/` (auth service)

- Для загрузки данных по фильмам, персонам и жанрам необходимо применить схему и создать таблицы:
    - `psql -U app -d api_database -f movies_database` в контейнере базы данных для Async API - `postgres_for_api`
- Запустить скрипты для переноса данных из SQLite в PostgreSQL и выполнения ETL-процесса - в контейнере `etl`:
    - выполнить скрипт `sqlite_to_postgres.sh`, выполнение переноса данных автоматически тестируются в выводом результата проверки
    - выполнить скрипт `start_etl.sh` для запуска ETL-процесса. Сохрание состояния происходит в файле:
    `./async_api/etl/postgres_to_es/state_storage.json`. При повторной выгрузке данных в Elasticsearch необходимо его удалить.

- ADMIN PANEL SERVICE (`django_admin_panel` <- наименование сервиса в docker-compose):
    - выполнена внешняя аутентификация - данные учетной записи отправляются на эндпоинт `auth/login/` сервиса аутентификации, откуда извлекаются данные пользователя в виде токена доступа. В нем содержатся основные данные пользователя, в частности, его права - токен декодируется и определяются права пользователя. При наличии прав (роли `admin` и `super_user`) авторизация проходит успешно, и пользователь заходит в сервис. Получив токен доступа, необходимо в интерактивной документации ввести его в поле JWTBearer.

- ASYNC API SERVICE (`backend_for_api`):
    - для получения ответа по эндопоинтам необходимо пройти авторизацию - сперва залогиниться через эндпоинт `auth/login/` сервиса аутентификации. Каждый эндпоинт обрабатывает зависимость по получению и декодированию токена для получения списка прав - перед выполнением запросов по эндпоинтам необходимо в интерактивной документации ввести его в поле JWTBearer.


- AUTH SERVICE (`backend_for_auth`):
    - Для запуска сервиса необходимо выполняется скрипт `./auth/run_auth_service.sh` после создания образа и контейнера. Перед запуском проекта применяться миграции Alembic.
    - Через декоратор добавлены проверка прав пользователя для авторизации (в проекте на текущий момент три роли: `public_user`, `admin`, `super_user`) при выполнении запросов по эндпоинтам сервиса.

    - Для создания пользователя можно воспользоватьcя следующей командой, находясь в корневой директории проекта: `python -m src.core.createsuperuser`.
    - Также используется декоратор для ограничения количества запросов к серверу.
    - Реализована трассировка запросов в Auth-сервис и подключен Jaeger. Для работы необходимо раскомментировать добавление в сервис middleware - файл `./auth/src/main.py` строки 81-90 - и запустить сервис Jaeger в docker-compose. По умолчанию трассировка отключена из-за необходимости наличия в заголовках запросов `X-Request-Id`, из-за чего отсутствует возможность регистрации и аутентификации пользователей через социальные сети.
    - Для доступа к эндпоинту `/auth/login` с других доменов настроен CORS.
    - Регистрация и аутентификация с использованием OAuth2 реализован протокол взаимодействия с Google API. Для регистрации необходимо перейти по эндпоинту `/oauth/`.