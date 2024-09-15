from pymongo import MongoClient

# Remplace par l'URL de connexion correcte si nécessaire
client = MongoClient('mongodb://localhost:27017/')

# Sélectionne la base de données
db = client['ProjetM1']

# Supprime la base de données
client.drop_database('ProjetM1')

print("La base de données 'ProjetM1' a été supprimée.")
