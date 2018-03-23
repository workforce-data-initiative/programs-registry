# -*- coding: utf-8 -*-

import os

from app.app import create_app


if __name__ == "__main__":
    port = int(os.getenv('PORT', '5000'))
    create_app().run(host="127.0.0.1", port=port)
