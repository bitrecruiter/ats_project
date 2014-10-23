"""
Django settings for ats_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import json
SECRETS = json.loads(open(os.path.join(BASE_DIR, "secrets.json"), 'r').read())


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRETS['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

ALLOWED_HOSTS = ['127.0.0.1']

ACCOUNT_ACTIVATION_DAYS = 7

# Application definition

SITE_ID = 1

INSTALLED_APPS = (
    'ats',
    'ats_profiles',
    'registration',
    'bcauth',
    'markdown_deux',
    'social.apps.django_app.default',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ats_project.urls'

WSGI_APPLICATION = 'ats_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'public')

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = '74.125.133.108'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'btctalent@gmail.com'
EMAIL_HOST_PASSWORD = 'alfierules3000'
DEFAULT_FROM_EMAIL = 'btctalent@gmail.com'
DEFAULT_TO_EMAIL = 'azelphur@azelphur.com'
SERVER_EMAIL = 'btctalent@gmail.com'

AUTHENTICATION_BACKENDS = (
    'social.backends.linkedin.LinkedinOAuth',
    'social.backends.github.GithubOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'bcauth.backends.BitcoinBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_LINKEDIN_KEY = '75qopsag3rc100'
SOCIAL_AUTH_LINKEDIN_SECRET = 'S4WZNt8Zlc8kQXXx'
SOCIAL_AUTH_GITHUB_KEY = '6e1e83cc9c24d7da83b3'
SOCIAL_AUTH_GITHUB_SECRET = 'b1e00cdf9587c7733c70f83e64299222ebe1ec5f'
SOCIAL_AUTH_FACEBOOK_KEY = '840188376011661'
SOCIAL_AUTH_FACEBOOK_SECRET = '237cd3389313c8d4185735f9fddccfbe'

BCAUTH_SESSION_EXPIRE = 60
BCAUTH_CHALLENGE = 'This message is being signed solely to authenticate to btcTalent on $timestamp. It is not to be used for any other purposes. It is void for any purpose after $expires. $otp'
