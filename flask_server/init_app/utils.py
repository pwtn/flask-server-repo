import config
from pymongo import MongoClient

client = MongoClient(config.mongo_url)
db = client[config.db_name]

def is_in_db(collection_name):
    return (collection_name in db.list_collection_names()) and (db[collection_name].estimated_document_count()!= 0)

def drop_collections():
    for col in config.collections:
        if is_in_db(col):
            db[col].drop()
            print("dropped collection %s..." %col)

    print("ready to load data...\n")
