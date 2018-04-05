# -*- coding: utf-8 -*-

import os

from app.app import create_app


config_name = os.environ.get('APP_SETTINGS', default='production')
port = int(os.environ.get('PORT', default='5000'))
host = os.environ.get('HOST', default="127.0.0.1")
application = create_app(config_name)

if __name__ == "__main__":
    application.run(host=host, port=port)