from .base import *

DEBUG = False

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
# STATIC_URL = '/new_static/'
# DATABASES = {
#  'default': {
#  # 'ENGINE': 'django.db.backends.mysql',
#  'ENGINE': 'mysql.connector.django',
#  'NAME': "leanjapan_dev2", # 接続するDB名
#  'USER': "leanjapan_d2user", # 接続ユーザ
#  'PASSWORD': "5t66rfCd32", # パスワード
#  'HOST': "mysql8056.xserver.jp", # ホスト名
#  'PORT': "3306", # ポート番号(3306固定)
#  'OPTIONS': {
#  # 'charset': 'utf8mb4',
#  'autocommit': True,
#  }
#  }
# }


####################################### New Database 03/03/2020 #########################################
DATABASES = {
 'default': {
 # 'ENGINE': 'django.db.backends.mysql',
 'ENGINE': 'mysql.connector.django',
 'NAME': "leanjapan_dev2", # 接続するDB名
 'USER': "leanjapan_d2user", # 接続ユーザ
 'PASSWORD': "5t66rfCd32", # パスワード
 'HOST': "mysql8056.xserver.jp", # ホスト名
 'PORT': "3306", # ポート番号(3306固定)
 'OPTIONS': {
 # 'charset': 'utf8mb4',
 'autocommit': True,
 }
 }
}

# DATABASES = {
#     'default': {
#         # 'ENGINE': 'django.db.backends.mysql',
#         'ENGINE': 'mysql.connector.django',
#         'NAME': os.environ["DB_NAME"],
#         'USER': os.environ["DB_USER"],
#         'PASSWORD': os.environ["DB_PASS"],
#         'HOST': os.environ["DB_HOST"],
#         'PORT': os.environ["DB_PORT"],
#         # 'TIME_ZONE': '+09:00',
#         'OPTIONS': {
#             # 'charset': 'utf8mb4',
#             'autocommit': True,
#         }
#     }
# }

# static files
#STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
