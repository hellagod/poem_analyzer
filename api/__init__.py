from flask import Flask, url_for
from flask_cors import CORS
from flask_pymongo import PyMongo
from modules.db.utils import collection_initialization


def create_app(config):

    app = Flask(__name__)
    app.config.from_object(config.API.SERVER)
    app.config['MONGO_URI'] = config.API.DATABASE.MONGO_URI
    app.static_folder = 'static'
    app.mongo = PyMongo(app)
    collection_initialization(app.mongo.db)

    CORS(app)

    with app.app_context():
        from api.app_utils import init_bp
        init_bp(app)
    print(app.url_map)
    return app
