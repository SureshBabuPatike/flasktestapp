
from __future__ import print_function

import os
import sys
import pprint

from .app import create_app
import settings


def get_settingsobj():
    settingsobj = os.environ.get('FLASK_SETTINGS', settings.DevConfig)

    if isinstance(settingsobj, str):
        settingsstr = settingsobj
        if ':' in settingsstr:
            module, callable = settingsstr.rsplit(':', 1)
        else:
            module, callable = settingsstr.rsplit('.', 1)
        import importlib
        mod = importlib.import_module(module)
        settingsobj = getattr(mod, callable)
        print(('settingsobj', repr(settingsobj)), file=sys.stderr)
    return settingsobj

app = create_app(get_settingsobj())
