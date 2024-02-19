"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path


import os

from celery.schedules import crontab
from dotenv import load_dotenv
from django.urls import reverse_lazy


load_dotenv()



DEBUG = os.environ['DEBUG']
SECRET_KEY = os.environ['SECRET_KEY']

BASE_DIR = Path(__file__).resolve().parent.parent




ALLOWED_HOSTS =[f'{os.environ["ALLOWED_HOSTS"]}']

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',

    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'rest_framework_swagger',
    'rest_framework',
    'corsheaders',
    "myapps.member",
    "myapps.core",
    "myapps.product",
    "myapps.order",
    'drf_spectacular',
    'celery',
    'rest_framework.authtoken'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'myapps.member.midelware.Jwtmidelware.JWTAuthenticateMiddleware'



]
REST_FRAMEWORK = {
    # YOUR SETTINGS
    # 'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'rest_framework.authentication.TokenAuthentication',
    # ]
'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
          'rest_framework.authentication.TokenAuthentication',
'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('Bearer',),
}
# REST_FRAMEWORK = {
#     # Use Django's standard `django.contrib.auth` permissions,
#     # or allow read-only access for unauthenticated users.
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
#     ]
# }

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',  # Replace with your Redis server details
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

DATABASES = {
    'default': {
        'ENGINE': os.environ['ENGINE'],
        'NAME': os.environ['NAME'],
        'USER': os.environ['PG_USER'],
        'PASSWORD':os.environ['PASSWORD'],
        'HOST':os.environ['HOST'],
        'PORT':os.environ['PORT'],
        

    }
}
SPECTACULAR_SETTINGS = {
    'TITLE': 'Your Project API',
    'DESCRIPTION': 'Your project description',

}

AUTHENTICATION_BACKENDS = ['myapps.member.backend.EmailOrUsernameModelBackend']
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



CORS_ORIGIN_ALLOW_ALL = True
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True




STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "member.CustomUser"
LOGIN_URL = reverse_lazy('core:login')


EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DEFAULT_FROM_EMAIL = 'faribarezaee321@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'faribarezaee321@gmail.com'
EMAIL_HOST_PASSWORD = 'aoop ifvp bylo sllb'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# set the celery broker url
# CELERY_BROKER_URL = 'redis://127.0.0.1:6379/1'

# set the celery result backend
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_BEAT_SCHEDULE = {
    'delete_inactive_users': {
        'task': 'myapps.member.tasks.send_nightly_email',
        'schedule': crontab(minute=0, hour=0),  # Run at midnight
    },
}
# set the celery timezone
CELERY_TIMEZONE = 'UTC'


CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
]
# CORS_ALLOW_CREDENTIALS = True