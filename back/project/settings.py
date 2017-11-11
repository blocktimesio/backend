import os
import environ
import mongoengine
from split_settings.tools import (optional, include)

if not os.environ.get('NO_LOAD_SETTINGS_LOCAL'):
    include(
        optional('settings_local.py')
    )

root = environ.Path(__file__) - 1
env = environ.Env(DEBUG=(bool, False))

if not os.environ.get('NO_LOAD_ENV_FILE'):
    env_path = (root - 1)('.env')
    if os.path.exists(env_path):
        environ.Env.read_env(env_path)

os.sys.path.insert(0, (root - 1))
os.sys.path.insert(0, (root - 1)('apps'))

DEBUG = env('DEBUG')

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(',')

INSTALLED_APPS = [
    'flat_responsive',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    'corsheaders',
    'django_extensions',
    'redactor',
    'rest_framework',
    'rest_framework_mongoengine',
    'solo',
    'templated_email',

    'apps.post',
    'apps.news',
    'apps.users',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [root('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {'default': env.db()}

MONGODB_DATABASES = {
    'default': {
        'name': 'blocktimes',
        'host': env('MONGO_HOST', default='localhost'),
        'port': 27017,
        'tz_aware': True,
    },
}

mongoengine.connect(
    db=MONGODB_DATABASES['default']['name'],
    host=MONGODB_DATABASES['default']['host']
)

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

SITE_ID = 1

USE_I18N = True
USE_L10N = True

TIME_ZONE = 'CET'

MEDIA_URL = '/media/'
MEDIA_ROOT = (root - 1)('media')

STATIC_URL = '/static/'
STATIC_ROOT = (root - 1)('static')

STATICFILES_DIRS = [
    root('static'),
]

EMAIL_CONFIG = env.email_url(
    'EMAIL_URL',
    default='smtp://localhost:25'
)

BASE_URL = env('BASE_URL')

ADMIN_SITE_HEADER = 'Block Times'

SOLO_CACHE_TIMEOUT = 60 * 2
SOLO_CACHE_PREFIX = 'blocktimes_solo'

FIXTURE_DIRS = [
    root('fixtures'),
]

AUTH_USER_MODEL = 'users.User'

BROKER_URL = env('CELERY_BROKER_URL', default='redis://localhost:6379')

CELERY_BROKER_URL = env('CELERY_BROKER_URL', default='redis://localhost:6379')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND_URL', default='redis://localhost:6379')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

MONGODB_HOST = env('MONGODB_HOST', default='localhost')
MONGODB_DB = env('MONGODB_DB', default='blocktimes')

SOCIAL_CRAWLER_THREAD_COUNT = env('SOCIAL_CRAWLER_THREAD_COUNT', default=10, cast=int)

REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}

CORS_ORIGIN_WHITELIST = (
    'admin.blocktimes.io',
    'blocktimes.io',
    'localhost:8000',
)

include('loggers.py')

if os.environ.get('LOAD_SETTINGS_LOCAL'):
    include(
        optional('settings_local.py')
    )
