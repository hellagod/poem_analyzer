from flask import Flask
from api.main_api import bp as main


def init_bp(app: Flask):
    app.register_blueprint(main, url_prefix='/main')


