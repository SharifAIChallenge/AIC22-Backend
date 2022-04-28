import os

ENV = os.environ.get('ENV', 'development')
exec("from AIC22_Backend.settings.%s import *" % ENV)
