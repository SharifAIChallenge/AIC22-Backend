import os

ENV = os.environ.get('ENV', 'test')
exec("from AIC22_Backend.settings.%s import *" % ENV)
