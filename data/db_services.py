import data.mongodb as mongodb
import pandas as pd

## CONNECT TO DB
dbname = mongodb.get_database()


def get_data(collection:str):
    """Enable User to get the raw data of a collection from the database
    
    Args:
        collection (str): collection name

    Returns:
        list: données de la table
    """
    return list(dbname[collection].find())


def get_data_group_by_sum(collection: str, group_field: str, sum_fields: [str], order: int):
    """
    Parameters:
    - collection (str): Le nom de la collection MongoDB à interroger.
    - group_field (str): Le champ selon lequel grouper les données.
    - sum_fields (list of str): Les champs pour lesquels calculer la somme.
    - order (int): 1 pour un tri ascendant et -1 pour un tri descendant sur le champ de groupement.
    
    Returns:
    - list: Les résultats de l'agrégation.
    """
    pipeline = [
        {"$unwind": "$results"},
        {
            "$group": {
                "_id": f"$results.{group_field}",
                **{field: {"$sum": f"$results.{field}"} for field in sum_fields}
            }
        },
        {"$sort": {"_id": order}}
    ]
    
    return list(dbname[collection].aggregate(pipeline))



#print(get_data_group_by_sum("eco2mix", "date", ["consommation", "ech_physiques", "eolien", "hydraulique", "nucleaire"]))

def transform_to_df(data:list):
    if not data:
        print("Aucune donnée trouvée.")
        return None

    results = data

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

    