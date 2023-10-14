from pymongo import MongoClient
from pymongo.database import Database
import certifi

# CONNECTION_STRING = "mongodb+srv://Hamad:CMIISIprojetvisualisation@cmiprojetm1.ojtjyuu.mongodb.net/"
CONNEXION_STRING = "mongodb://localhost:27017/"
DB_NAME = "FranceEnergie"

def get_database(path = CONNEXION_STRING, dbname = DB_NAME):
   client = MongoClient(path, tlsCAFile=certifi.where())
   return client[dbname]

def create_collection(db: Database, name: str):
   if(not (name in db.list_collection_names())):
      db.create_collection(name)

def drop_collection(db: Database, name: str):
   if(name in db.list_collection_names()):
      db.drop_collection(name)

def insert_in_coll(db: Database, table_name: str, data: dict):
   db.get_collection(table_name).insert_one(data)

def insert_many_in_coll(db: Database, table_name: str, data: list):
    db.get_collection(table_name).insert_many(data)

def get_data(db: Database, table_name:str):
   return list(db[table_name].find())