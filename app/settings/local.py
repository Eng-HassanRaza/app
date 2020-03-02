from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, "db.sqlite3"),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': 'jpsocialdb',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# RunServerPlus
RUNSERVERPLUS_SERVER_ADDRESS_PORT = '0.0.0.0:8000'
