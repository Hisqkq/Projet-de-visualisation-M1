from pymongo import MongoClient
import certifi

# CONNECTION_STRING = "mongodb+srv://Hamad:CMIISIprojetvisualisation@cmiprojetm1.ojtjyuu.mongodb.net/"
CONNEXION_STRING = "mongodb://localhost:27017/"
DB_NAME = "FranceEnergie"

def get_database(path = CONNEXION_STRING, dbname = DB_NAME):
   client = MongoClient(path, tlsCAFile=certifi.where())
   return client[dbname]