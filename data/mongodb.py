### Permet la connexion avec la base de données
from pymongo import MongoClient
import configparser

config = configparser.ConfigParser()
config.read('data/config.ini')

# Provide the mongodb atlas url to connect python to mongodb using pymongo
CONNECTION_STRING = config.get('MongoDB', 'connection_path')

def get_database(path: str = CONNECTION_STRING):
   """Get the database
   
   Returns
   -------
   Database
       The database.
   """
   # Create a connection using MongoClient.
   client = MongoClient(path)
 
   # Create the database
   return client['ProjetM1']
  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
  
   # Get the database
   dbname = get_database()
 
