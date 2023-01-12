import http
import random

from flask import current_app
from flask_pymongo import PyMongo
from flask_pymongo.wrappers import Collection

from configs.config import settings

coll_name = settings.API.DATABASE.COLLECTIONS.POEM


def get_poem():
    mongo: PyMongo = current_app.mongo
    mongo_db = mongo.db
    coll: Collection = mongo_db.get_collection(coll_name)
    return {'text': dict(coll.find().limit(-1).skip(random.randint(1, coll.count_documents({}))).next()).get(
        'text')}, http.HTTPStatus.OK
