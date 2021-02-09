import os

if os.environ.get('environment'):
    exec('from settings.{} import *'.format(os.environ.get('environment')))
else:
    from settings.local import *
