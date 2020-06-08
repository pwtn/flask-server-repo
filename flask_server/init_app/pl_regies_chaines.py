from pymongo import MongoClient
import pandas as pd
import numpy as np
import config

# the file used comes from a extract from the software popcorn
# we basically have the same table that comes from the edi website
# we could also run the pipeline from that one
data_path = 'flask_server/init_app/data/popcorn_chaines_regies.xls'


def create_regies():
    # read the data
    df = pd.read_excel(data_path, dtype={'startDate':np.datetime64,'endDate':np.datetime64})

    # drop the chaines that are not associated to the regies anymore
    df = df[df.endDate >= np.datetime64('2020-01-01')]

    # keep and rename the relevant fields
    df = df[['regieLibelle', 'regieSymbole']].rename(columns={'regieLibelle': 'libelle', 'regieSymbole':'code'})

    # explicit
    df = df.drop_duplicates()

    # prepare as dict to be loaded into the database
    data = df.to_dict(orient='records')
    for elt in data:
        elt['chaines'] = []

    # launch the db work
    client = MongoClient(config.mongo_url)
    db = client[config.db_name]
    collection = db[config.col_regies]
    collection.insert_many(data)
    print("**** collection regies created ****")


def create_chaines():
    # read the data
    df = pd.read_excel(data_path, dtype={'startDate':np.datetime64,'endDate':np.datetime64})

    # drop the chaines that are not associated to the regies anymore
    df = df[df.endDate >= np.datetime64('2020-01-01')]

    # keep and rename the relevant fields
    df = df[['chaineSymbole', 'chaineLibelle', 'regieLibelle']].rename(columns={'chaineLibelle' : 'libelle', 'chaineSymbole': 'code' , 'regieLibelle': 'regie'})

    # prepare the data for insertion
    data = df.to_dict(orient='records')
    # for each chaine, find the corresponding regie in the db, to refer to it

    # launch the db work
    client = MongoClient(config.mongo_url)
    db = client[config.db_name]
    collection_regies = db[config.col_regies]
    collection_chaines = db[config.col_chaines]
    for chaine in data :
        regie_str = chaine['regie']
        regie = collection_regies.find_one({'libelle': regie_str})
        chaine['regie'] = regie['_id']
        collection_chaines.insert_one(chaine)
        collection_regies.update_one({'_id': regie['_id']},{'$push': {'chaines': chaine['_id']}})

    print('**** collection chaines created and collection regies updated  ****')
