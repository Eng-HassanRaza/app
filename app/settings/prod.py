from .base import *

DEBUG = False
FILE_UPLOAD_MAX_MEMORY_SIZE = 100000000
FILE_UPLOAD_PERMISSIONS=0o640

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
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

####################################### New Database 03/06/2020 #########################################
# DATABASES = {
#  'default': {
#  # 'ENGINE': 'django.db.backends.mysql',
#  'ENGINE': 'mysql.connector.django',
#  'NAME': "leanjapan_main", # 接続するDB名
#  'USER': "leanjapan_miuser", # 接続ユーザ
#  'PASSWORD': "ZiV7rekJ3uz", # パスワード
#  'HOST': "mysql8056.xserver.jp", # ホスト名
#  'PORT': "3306", # ポート番号(3306固定)
#  'OPTIONS': {
#  # 'charset': 'utf8mb4',
#  'autocommit': True,
#  }
#  }
# }

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
