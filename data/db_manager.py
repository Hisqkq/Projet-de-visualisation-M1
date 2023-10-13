import data.mongodb as mongodb
import pandas as pd

db = mongodb.get_database()

def create_collection(db, name):
    if(not (name in db.list_collection_names())):
        db.create_collection(name)

def drop_collection(db, name):
    if(name in db.list_collection_names()):
        db.drop_collection(name)

def insert_in_coll(db, table_name:str, data:dict):
    db.get_collection(table_name).insert_one(data)

def insert_many_in_coll(db, table_name:str, data:list):
    db.get_collection(table_name).insert_many(data)
    
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

    
# TODO:   
#print(data_to_df("sum_cons_par_regions"))

