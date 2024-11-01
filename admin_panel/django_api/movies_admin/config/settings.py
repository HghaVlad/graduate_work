import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include


dotenv_path = Path('movies_admin/.env')
load_dotenv(dotenv_path=dotenv_path)

include(
    'components/database.py',
)

BASE_DIR = Path(__file__).resolve().parent.parent

PUBLIC_KEY_PATH: Path = Path(__file__).resolve().parent.parent / 'certs' / 'public.pem'

ALGORITHM = 'RS256'

SECRET_KEY = os.environ.get('SECRET_KEY')

#DEBUG = os.environ.get('DEBUG', False) == 'True'
DEBUG = True

ALLOWED_HOSTS: str = ["*"]

INTERNAL_IPS = [
    '127.0.0.1',
    '172.26.0.1',  # Gateway IP address of Django Container
]

INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'corsheaders',
    "rest_framework",
    # Local
    'movies',
    "profiles",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    INSTALLED_APPS.insert(-1, 'debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    'accounts.auth.CustomBackend',
    # 'django.contrib.auth.backends.ModelBackend'
]

AUTH_API_LOGIN_URL = 'http://backend_for_auth:8000/auth/login/'

LANGUAGE_CODE = 'en-US'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_ROOT = BASE_DIR / 'static/'

STATIC_URL = 'static/'

MEDIA_ROOT = BASE_DIR / 'media/'

MEDIA_URL = 'media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOCALE_PATHS = ['movies/locale']

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8085',
    'http://localhost:8002',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50
}
