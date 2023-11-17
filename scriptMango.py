# fichier temporaire pour réorganiser le code
# TODO: supprimer

import requests
from pymongo import MongoClient

CONNEXION_STRING = "mongodb://localhost:27017/"
DATA_SET_ID = "eco2mix-regional-tr"

def fetch_data(datasetID, rows = 100, sort = ""):
    url = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/"
    url += datasetID + "/records"
    params = {
        "rows": rows,
        "sort": sort
    }
    response = requests.get(url, params=params)
    data=[{}]
    if response.status_code == requests.codes.ok:
        data = response.json()
        return data
    else:
        print(f"Échec de la requête: {response.status_code}")
        print(response.text)
        return data

def get_database(path):
    client = MongoClient(path)
    return client['FranceEnergie']

def create_collection(db, name):
    if(not (name in db.list_collection_names())):
        db.create_collection(name)

def drop_collection(db, name):
    if(name in db.list_collection_names()):
        db.drop_collection(name)

def insert_in_coll(db, table_name:str, data:dict):
    db.get_collection(table_name).insert_one(data)

db = get_database(CONNEXION_STRING)

# drop_collection(db, "éCO2mix")

data = fetch_data(DATA_SET_ID, 100) # peut-être additionner les données de plusieurs fetchs avant de les insérer dans la base de données
create_collection(db, "éCO2mix")
insert_in_coll(db, "éCO2mix", data)