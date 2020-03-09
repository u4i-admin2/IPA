# coding: utf-8

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += (
    'storages',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('DATABASE_NAME'),
        'USER': get_env_variable('DATABASE_USER'),
        'PASSWORD': get_env_variable('DATABASE_PASSWORD'),
        'HOST': get_env_variable('DATABASE_HOST'),
        'PORT': '',  # Set to empty string for default.
    },
}

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': 'united_cache',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

AWS_S3_OBJECT_PARAMETERS = {
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'CacheControl': 'max-age=94608000',
}

# Tell django-storages the domain to use to refer to static files.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# Media Files
MEDIA_ROOT = os.path.join(BASE_DIR, 'MEDIA')
MEDIA_URL = '/media/'

DEFAULT_FILE_STORAGE = 'ipa.media_storage.MediaStorage'
THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE
MEDIAFILES_LOCATION = 'media'

# Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
# you run `collectstatic`).
STATICFILES_STORAGE = 'ipa.media_storage.StaticStorage'
STATICFILES_LOCATION = 'static'

LOG_LEVEL = 'ERROR'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s %(levelname)s %(name)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'null': {
            'class': 'logging.NullHandler',
        },
        'django': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose'
        },
        'application': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['django'],
            'level': LOG_LEVEL
        },
        'django.template': {
            'handlers': ['django'],
            # Allowing django.template to log with a LOG_LEVEL of
            # 'DEBUG' generates mountains of harmless
            # VariableDoesNotExist exceptions because of core admin
            # templates attempting to access undefined context keys.
            # This is a core bug we can’t work around without overriding
            # a lot of core templates.
            'level': 'INFO' if LOG_LEVEL == 'DEBUG' else LOG_LEVEL
        },
        'django.db.backends': {
            'handlers': ['null'],
            'level': LOG_LEVEL,
            'propagate': False
        },
        'django.request': {
            'handlers': ['django'],
            'level': LOG_LEVEL
        },
        'public': {
            'handlers': ['application'],
            'level': LOG_LEVEL
        },
    },
}

"""
Remember to run python manage.py createcachetable if using DB cache!!!!
"""
