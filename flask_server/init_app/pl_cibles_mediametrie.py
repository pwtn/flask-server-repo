import config

import pandas as pd
from pymongo import MongoClient

data_path = "flask_server/init_app/data/Cibles standard et Marché.xlsx"
df = pd.read_excel(data_path, skiprows = 1, usecols = [1, 3])

# separate two sets of targets
cibles_std = df['Cibles standard 2020'].dropna().rename("cible")
cibles_marche = df['Cibles Marché'].dropna().rename("cible")

# add metafields 'fournisseur' and 'description'
df_std = pd.DataFrame(cibles_std)
df_std['fournisseur'], df_std['description'] = 'Médiamétrie', 'Cibles Standard'

df_marche = pd.DataFrame(cibles_marche)
df_marche['fournisseur'], df_marche['description'] = 'Médiamétrie', 'Cibles Marché'

# concat into one db
df = pd.concat([df_std, df_marche], axis=0).reset_index(drop = True)

# transform to dict
data = df.to_dict(orient='records')

def create_cibles():
    client = MongoClient(config.mongo_url)
    db = client[config.db_name]
    collection = db[config.col_cibles]
    collection.insert_many(data)
    print("**** collection cibles created ****")

# not working on atlas because of a dns library issue
# create_cibles()
