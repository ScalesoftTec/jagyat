
from pathlib import Path
import os

import environ
BASE_DIR = Path(__file__).resolve().parent.parent


env = environ.Env()
environ.Env.read_env()



import base64
raw_pass = env('DATABASE_PASS')

if  env('AWS_SECRET_KEY'):
    DATABASE_PASS = base64.b64decode(raw_pass).decode('utf-8')
else:
    DATABASE_PASS = raw_pass


# Build paths inside the project like this: BASE_DIR / 'subdir'.

SECRET_KEY = env('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'storages',
    'django_crontab',
    'django.contrib.sites',
    "debug_toolbar",
    "corsheaders",
    'rest_framework',
    'import_export',
    'django.contrib.humanize',
    'django_filters',
    'mathfilters',
    'django_cleanup.apps.CleanupConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor', # CKEditor config
    'ckeditor_uploader', # CKEditor media uploader
    'dashboard.apps.DashboardConfig',
    'masters.apps.MastersConfig',
    'accounting.apps.AccountingConfig',
    'api.apps.ApiConfig',
    'home.apps.HomeConfig',
    'easyaudit',
    
    'crm.apps.CrmConfig',
    'business_intelligence.apps.BusinessIntelligenceConfig',
    'hr.apps.HrConfig',
    'operations.apps.OperationsConfig',
    'accounting_report.apps.AccountingReportConfig',
 
]

SITE_ID = 1



STATIC_URL = 'static/'  
MEDIA_URL = 'media/'

if env('AWS_SECRET_KEY'):
    
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    
    AWS_ACCESS_KEY_ID = env('AWS_SECRET_KEY')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS')
    AWS_STORAGE_BUCKET_NAME = 'jagyat-bucket'
    AWS_S3_REGION_NAME = 'ap-south-1' 
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_S3_FILE_OVERWRITE = False

    STORAGES = {

        # Media file (image) management  
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage", 
            "OPTIONS": {
                "location": "media",  # <-- this adds the prefix!
            },
        },

        # CSS and JS file management
        "staticfiles": {
            "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
        },
    }



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'dashboard.middleware.OneSessionPerUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'easyaudit.middleware.easyaudit.EasyAuditMiddleware',
    
]

ROOT_URLCONF = 'SDI_FFS_PROJECT.urls'

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
                'dashboard.context_processors.alerts_messages'
            ],
        },
    },
]

WSGI_APPLICATION = 'SDI_FFS_PROJECT.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DATABASE_NAME'),
        'PORT': env('DATABASE_PORT'),
        'USER': env('DATABASE_USER'),
        'HOST': env('DATABASE_HOST'),
        'PASSWORD': DATABASE_PASS,
        
    }
}


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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


IMPORT_EXPORT_SKIP_ADMIN_LOG = True

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}


#ckeditor upload path
CKEDITOR_UPLOAD_PATH="uploads/"
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = 'jarvis12g@gmail.com'
EMAIL_HOST_PASSWORD = 'xfgmygaxaekqwbpg'
EMAIL_USE_TLS = True

CRONJOBS = [
    ('0 20 * * *', 'home.cron.todayUpdates')
]

CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOWED_ORIGINS = []

CORS_ALLOW_METHODS = [
    "GET",
]

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "my_cache_table",
    }
}
