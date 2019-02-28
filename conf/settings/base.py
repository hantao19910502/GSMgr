import os
from os.path import join, abspath, dirname

here = lambda *dirs: join(abspath(dirname(__file__)), *dirs)
BASE_DIR = here("..", "..")
root = lambda *dirs: join(abspath(BASE_DIR), *dirs)
# BASE_DIR = os.path.dirname(os.path.dirname(__file__) + "/..")


ROOT_URLCONF = 'conf.urls'

#WSGI_APPLICATION = 'babel_ops.wsgi.application'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = "userinfo.User"
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
ALLOWED_HOSTS = ['*']
SALT_DIR = BASE_DIR
SESSION_COOKIE_AGE = 3 * 60 * 60
