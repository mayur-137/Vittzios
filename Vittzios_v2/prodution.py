from .settings import *

DEBUG = False

ALLOWED_HOSTS = ["15.206.194.134"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Wholesome',
        'USER': 'admin_Wholesome',
        'PASSWORD': 'Wholesome#2510',  # dfGhj567
        'HOST': 'wholesome.ckeoq85gknjy.ap-south-1.rds.amazonaws.com',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'STRICT_ALL_TABLES',
        },
    }
}