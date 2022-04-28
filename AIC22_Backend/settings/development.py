from AIC22_Backend.settings.base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'aic_database',
        'HOST': '127.0.0.1',
        'USER': 'aic',
        'PASSWORD': '123',
        'PORT': '5432',
        'AUTOCOMMIT': True,
    },
}
