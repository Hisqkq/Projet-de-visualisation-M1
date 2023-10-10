from pymongo import MongoClient
import api_service
def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://Hamad:CMIISIprojetvisualisation@cmiprojetm1.ojtjyuu.mongodb.net/"

   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['ProjetM1']
  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
  
   # Get the database
   dbname = get_database()
   if(not ("sum_cons_par_regions" in dbname.list_collection_names())):
      dbname.create_collection("sum_cons_par_regions")
   
   dbname.get_collection("sum_cons_par_regions").insert_one(api_service.json_data_consommation_quotidienne_brute())