import json
import os

from django.core.exceptions import ImproperlyConfigured

with open(os.environ.get('CONFIG')) as f:
    configs = json.loads(f.read())

def get_env_var(setting, configs=configs):

    try:
        val = configs[setting]
        if val == 'True':
            val = True
        elif val == 'False':
            val = False
        return val

    except KeyError:
        error_msg = "improperlyConfigured: Set {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)