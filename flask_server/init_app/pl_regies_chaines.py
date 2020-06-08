from pymongo import MongoClient
import pandas as pd
import numpy as np
import config



def create_regies():
    data_path = 'flask_server/init_app/data/popcorn_chaines_regies.xls'

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
