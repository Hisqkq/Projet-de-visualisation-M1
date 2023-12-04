### Permet la connexion avec la base de données
from pymongo import MongoClient

def get_database():
   """Get the database
   
   Returns
   -------
   Database
       The database.
   """
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb://localhost:27017"

   # Create a connection using MongoClient.
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database
   return client['ProjetM1']
  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
  
   # Get the database
   dbname = get_database()
 
