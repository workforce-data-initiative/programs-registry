import os

from app import create_app as application

config_name = os.getenv('APP_SETTINGS')
app = application(config_name)
if __name__ == "__main__":
    app.run()

