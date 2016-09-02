# -*- coding: utf-8 -*-
"""Create an application instance."""
import os

from flasktestapp.app import create_app
from flasktestapp.settings import DevConfig, ProdConfig

CONFIG = ProdConfig if os.environ.get('FLASKTESTAPP_ENV') == 'prod' else DevConfig

app = create_app(CONFIG)
