### Permet de gérer la base de données directement avec des get, insert, create collection (table) etc...
 
import data.mongodb as mongodb
import pandas as pd

## CONNECT TO DB
dbname = mongodb.get_database()

def create_collection(name:str):
    """Permet de créer une nouvelle table dans la database

    Args:
        name (str): nom de la base de données
    """
    if(not (name in dbname.list_collection_names())):
        dbname.create_collection(name)

#test
#create_collection("sum_cons_par_regions")
   

## ADD DATA (Json) IN A TABLE
def insert_in_coll(table_name:str, data:dict):
    """Ajoute des données à une table existante

    Args:
        table_name (str): nom de la table visée
        data (dict): données à injecter
    """
    dbname.get_collection(table_name).insert_one(data)

#test
#insert_in_coll("sum_cons_par_regions", api_service.json_data_consommation_quotidienne_brute())


def get_data(table_name:str):
    """Permet de récupérer les données d'une table

    Args:
        table_name (str): nom de la table visée

    Returns:
        list: données de la table
    """
    return list(dbname[table_name].find())


def data_to_df(table_name:str):
    """return the dataframe of a table from the database

    Args:
        table_name (str): name of the table from the database

    Returns:
        Dataframe: pandas dataframe
    """
    data = get_data(table_name)
    
    if not data:
        print("Aucune donnée trouvée.")
        return None

    results = data[0].get('results', [])

    if not results:
        print("Pas de résultats dans les données.")
        return None
    
    try:
        dataframe = pd.DataFrame(results)
        return dataframe
    except pd.errors.EmptyDataError:
        print("Aucune donnée à charger dans le DataFrame.")
        return None
    except Exception as e:
        print("Une erreur inattendue s'est produite :", str(e))
        return None

    
#test   
#print(data_to_df("sum_cons_par_regions"))

