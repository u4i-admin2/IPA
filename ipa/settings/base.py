# coding: utf-8

"""
Django settings for ipa project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.urls import reverse_lazy
from django.core.exceptions import ImproperlyConfigured
import os
import sys
import random
import string

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.dirname(BASE_DIR)
SECRET_KEY = os.environ.get('SECRET_KEY')

def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise ImproperlyConfigured(error_msg)


AEA_HOSTNAME = get_env_variable('AEA_HOSTNAME')
IPA_HOSTNAME = get_env_variable('IPA_HOSTNAME')

SHOW_SISTER_SITE_LINK = os.environ.get('SHOW_SISTER_SITE_LINK', None) == 'true'

AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', None)
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', None)
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
AWS_CLOUDFRONT_DISTRIBUTION_ID = os.environ.get('AWS_CLOUDFRONT_DISTRIBUTION_ID', None)
VERSION_NUM = os.environ.get('VERSION_NUM', 'NA')
BUILD_NUM = os.environ.get('BUILD_NUM', 'NA')
GIT_SHORT_SHA = os.environ.get('GIT_SHORT_SHA', 'NA')

ALLOWED_HOSTS = [
    AEA_HOSTNAME,
    IPA_HOSTNAME,
]

DEFAULT_HOST = 'ipa'

ROOT_HOSTCONF = 'ipa.hosts'

# Application definition
INSTALLED_APPS = [
    'flat',
    'django.contrib.sites',
    'modeltranslation',
    'public',
    'ui',
    'admin_assets',
    'allauth',
    'allauth.account',
    'logentry_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    'django_extensions',
    'django_hosts',
    'django_nose',
    'django_select2',
    'easy_thumbnails',
    'image_cropping',
    'rest_framework',
    'watson',
    'adminsortable',
    'markdownx',
    'nested_admin',

    'core_types',
    'ipa',
    'prisoners',
    'api',
    'judges',
    'prisons',
    'report',
    'news',
]

SITE_ID = 1

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

MIDDLEWARE_CLASSES = [
    'ipa.middleware.RevisionMiddleware',
    'django_hosts.middleware.HostsRequestMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'api.middleware.ResponseManipulationMiddleware',
    'ipa.middleware.ResponseManipulationMiddleware',
    'public.middleware.ResponseAndViewManipulationMiddleware',
    'ui.middleware.ResponseManipulationMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

ROOT_URLCONF = 'ipa.urls'

WSGI_APPLICATION = 'ipa.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-source'
ADMIN_LANGUAGE_CODE = 'en'

gettext = lambda s: s
LANGUAGES = (
    ('fa', gettext('Persian')),
    ('en', gettext('English')),
    ('en-source', 'English (source)'),
)
MODELTRANSLATION_LANGUAGES = (
    'fa',
    'en',
)
MODELTRANSLATION_DEFAULT_LANGUAGE = 'fa'
MODELTRANSLATION_FALLBACK_LANGUAGES = (
    'fa',
    'en'
)

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
MEDIA_URL = '/media/'

LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, 'locale'),
)

APP_SUPERUSER_GROUP_NAME = 'Publishing Managers'

AUTHENTICATION_BACKENDS = (

    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',

)
#
# django.contrib.auth configuration.
#
LOGIN_URL = reverse_lazy('ui:users:login')
LOGIN_REDIRECT_URL = reverse_lazy('ui:dashboard:home')

#
# Configuration for our app.
#
WATSON_BACKEND = "watson.backends.PostgresSearchBackend"
API_THUMB_SIZE = (160, 160)


from easy_thumbnails.conf import Settings as thumbnail_settings
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS

PRISONERS_CSV_FILE_KEY_NAME = 'csv/prisoners.csv'

# ===========================
# === Public app settings ===
# ===========================

AEA_PRISON_ADMINISTERED_BY_WHITELIST = (
    'pdotj',
    'police',
)
