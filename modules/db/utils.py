from flask_pymongo.wrappers import Database
from configs.config import settings


def collection_initialization(db: Database):
    names = db.list_collection_names()
    new_names = [settings.API.DATABASE.COLLECTIONS.POEM]
    for name in new_names:
        if name not in names:
            db.create_collection(name)