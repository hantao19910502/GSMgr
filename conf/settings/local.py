from .base import *

import djcelery

djcelery.setup_loader()
BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

DEBUG = True
TEMPLATE_DEBUG = True
# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'userinfo',
    'openserver',
    'mergerserver',
    'api',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.CacheMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django.core.files.uploadhandler.MemoryFileUploadHandler',
    #'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },

}
#DATABASE_ROUTERS = ['dns.route.DNSRouter']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'gsmgr',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}
AUTHENTICATION_BACKENDS = ('userinfo.views.BournceBackend',)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
AUTH_USER_MODEL = "userinfo.User"
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATIC_URL = '/static/'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + "/templates/"],
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
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ("liudechuan", "liudechuan@babeltime.com")
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'formatter': 'standard',
        },
        'perm.views': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'formatter': 'standard',
        },
    },
}

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "upload"),
)
SECRET_KEY = 'f_+f0uz3pj8=uqw3jrxbet06enb2jpa7+43!3cqzrf#7g+u27d'
ALLOWED_HOSTS = ['*']
UPLOAD_DIR = BASE_DIR + "/upload/"
SALT_DIR = BASE_DIR + "/s/init/"
SALT_API = 'https://192.168.9.11:8000'
HOST_PORT = "127.0.0.1:8000"
SCRIPT_CACHE_DIR = BASE_DIR + "/backend/module/mergegame/tmp"
