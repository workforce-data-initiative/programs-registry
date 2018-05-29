# -*- coding: utf-8 -*-

import os

from program_registry import create_app


config_name = os.environ.get('FLASK_ENV', default='production')
port = int(os.environ.get('FLASK_RUN_PORT', default='5000'))
host = os.environ.get('FLASK_RUN_HOST', default="127.0.0.1")
application = create_app(config_name)

if __name__ == "__main__":
    application.run(host=host, port=port)