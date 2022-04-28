import os

from AIC22_Backend.settings.base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'HOST': os.getenv('DATABASE_HOST'),
        'USER': os.getenv('DATABASE_USERNAME'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'PORT': os.getenv('DATABASE_PORT', '5432'),
        'AUTOCOMMIT': True,
    },
}
