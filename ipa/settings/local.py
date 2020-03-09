# coding: utf-8

import os
import sys

from .base import * # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

should_show_django_debug_toolbar = True

local_use_s3_storage_media = (
    os.environ.get('LOCAL_USE_S3_STORAGE_MEDIA', None) == 'true'
)
local_use_s3_storage_static = (
    os.environ.get('LOCAL_USE_S3_STORAGE_STATIC', None) == 'true'
)

if local_use_s3_storage_media or local_use_s3_storage_static:
    AWS_S3_OBJECT_PARAMETERS = {
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'CacheControl': 'max-age=94608000',
    }

    # Tell django-storages the domain to use to refer to static files.
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

    # Media Files
    MEDIAFILES_LOCATION = 'media'

    if local_use_s3_storage_media:
        print(u'Using S3 bucket {bucket_name} for media'.format(
            bucket_name=AWS_STORAGE_BUCKET_NAME
        ))

        MEDIA_ROOT = os.path.join(BASE_DIR, 'MEDIA')
        MEDIA_URL = '/media/'

        DEFAULT_FILE_STORAGE = 'ipa.media_storage.MediaStorage'
        THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE

    # Tell the staticfiles app to use S3Boto3 storage when writing the collected static files (when
    # you run `collectstatic`).
    STATICFILES_LOCATION = 'static'

    if local_use_s3_storage_static:
        print(u'Using S3 bucket {bucket_name} for static'.format(
            bucket_name=AWS_STORAGE_BUCKET_NAME
        ))

        STATICFILES_STORAGE = 'ipa.media_storage.StaticStorage'

    should_show_django_debug_toolbar = False

if DEBUG and should_show_django_debug_toolbar:
    INSTALLED_APPS += (
        'debug_toolbar',
        # 'template_timings_panel',
    )

    INTERNAL_IPS = (
        '127.0.0.1',
    )

    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
        # 'template_timings_panel.panels.TemplateTimings.TemplateTimings',
    ]

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }

    def show_toolbar(request):
        return True

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
        'RESULTS_CACHE_SIZE': 100
    }

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

# Note: DatabaseCache could be useful to improve performance when
# testing the AngularJS components, but shouldn’t be used when
# developing Django code
CACHES = {
    'default': {
        # 'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': 'united_cache',
    }
}

LOG_LEVEL = 'DEBUG'

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
        'report.admin': {
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
        'api': {
            'handlers': ['application'],
            'level': LOG_LEVEL
        },
        'ipa': {
            'handlers': ['application'],
            'level': LOG_LEVEL
        },
        'public': {
            'handlers': ['application'],
            'level': LOG_LEVEL
        },
        'ui': {
            'handlers': ['application'],
            'level': LOG_LEVEL
        },
    },
}
