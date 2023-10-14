### Permet de gérer la base de données directement avec des get, insert, create collection (table) etc...
 
import mongodb as mongodb
import pandas as pd
import api_service as api_service
import time
import datetime

## CONNECT TO DB
dbname = mongodb.get_database()

def create_collection(name:str):
    """Permet de créer une nouvelle collection dans la database

    Args:
        name (str): nom de la base de données
    """
    if(not (name in dbname.list_collection_names())):
        dbname.create_collection(name)

#test
#create_collection("eco2mix")
#dbname.drop_collection("eco2mix")
   

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


def insert_data(collection_name:str, start_date:str, end_date:datetime):
    """Permet de remplir une base de donnée jourr par jourr 100 lignes par 100 ligne

    Args:
        collection_name (str): nom de la collection 
        start_date (str): date de départ (api_service.get_first_date(collection_name))
        end_date (datetime): dernière date dans le dataframe
    """
    step = 100
    lines_per_date = 1056 
    
    current_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = end_date
    
    while current_date <= end_date:
        formatted_date = current_date.strftime('%Y-%m-%d') 
        print(formatted_date)
        
        for i in range(0, lines_per_date, step):
            rows = min(step, lines_per_date - i)
            try:
                data = api_service.fetch_eco2mix(i, rows, str(formatted_date))
                
                if isinstance(data, list):
                    dbname.get_collection(collection_name).insert_many(data)
                else:
                    dbname.get_collection(collection_name).insert_one(data)
                    
            except Exception as e:
                print(f"Erreur lors de l'insertion des données pour la date {formatted_date}, offset {i}: {e}")
                print("Réessai dans 5 secondes...")
                time.sleep(5)  
                i -= step  
                continue
                
        current_date += datetime.timedelta(days=1)


        
insert_data("eco2mix", api_service.get_first_date("eco2mix-regional-tr"), datetime.datetime.now())

"""
data = {
    "step": 100,
    "offset": 0
}


insert_in_coll("config", data)
"""
