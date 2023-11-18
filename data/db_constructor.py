import requests
import mongodb
import datetime
import time

## CONNECT TO DB
dbname = mongodb.get_database()
    
###### API ######     
    
def fetch_data_by_date(data, start, rows, date):
    url = f"https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/{data}/records"
    params = {
        "offset" : start,
        "rows": rows,
        "where": f"date='{date}'"
    }
    response = requests.get(url, params=params)
    data=[{}]
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Échec de la requête: {response.status_code}")
        print(response.text)
        return 
    
def get_dataset_lenght(dataset:str):
    url = "https://odre.opendatasoft.com/api/records/1.0/search/"
    params = {
        "dataset": dataset,
        "rows": 1
    }
    response = requests.get(url, params=params)  
    if response.status_code == 200:
        data = response.json()
        return int(data.get('nhits', []))
    else:
        print(f"Échec de la requête: {response.status_code}")
        print(response.text)
        return 0
    
def get_first_date(dataset:str):
    """get the minimum date in a dataset

    Args:
        dataset (str): _description_

    Returns:
        _type_: _description_
    """
    url = f"https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/{dataset}/records"
    params = {
        "select": "date",
        "rows": 1,
        "order_by": "date",
    }
    response = requests.get(url, params=params)
    data=[{}]
    if response.status_code == 200:
        data = response.json()
        return data.get('results')[0]['date']
    else:
        print(f"Échec de la requête: {response.status_code}")
        print(response.text)
        return
    
def get_last_date(dataset:str):
    """get the maximum date in a dataset

    Args:
        dataset (str): _description_

    Returns:
        _type_: _description_
    """
    url = f"https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/{dataset}/records"
    params = {
        "select": "date",
        "rows": 1,
        "order_by": "-date",
    }
    response = requests.get(url, params=params)
    data=[{}]
    if response.status_code == 200:
        data = response.json()
        return data.get('results')[0]['date']
    else:
        print(f"Échec de la requête: {response.status_code}")
        print(response.text)
        return
    
def get_length_per_date(dataset:str, date:str):
    """get the minimum date in a dataset

    Args:
        dataset (str): _description_

    Returns:
        _type_: _description_
    """
    url = f"https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/{dataset}/records"
    params = {
        "select": "date",
        "rows": 1,
        "where": f"date='{date}'"
    }
    response = requests.get(url, params=params)
    data=[{}]
    if response.status_code == 200:
        data = response.json()
        return data.get('total_count')
    else:
        print(f"Échec de la requête: {response.status_code}")
        print(response.text)
        return
    
    
    
###### Construction ######     
    
def create_collection(name:str):
    """Permet de créer une nouvelle collection dans la database

    Args:
        name (str): nom de la base de données
    """
    if(not (name in dbname.list_collection_names())):
        dbname.create_collection(name)    
    
def insert_one_in_coll(table_name:str, data:dict):
    """Ajoute des données à une table existante

    Args:
        table_name (str): nom de la table visée
        data (dict): données à injecter
    """
    dbname.get_collection(table_name).insert_one(data)
    
def insert_many_in_coll(table_name:str, data:list):
    """Ajoute des données à une table existante

    Args:
        table_name (str): nom de la table visée
        data (dict): données à injecter
    """
    dbname.get_collection(table_name).insert_many(data)
    
def get_last_date_db(collection):
    pipeline = [
        {"$unwind": "$results"},
        {"$sort": {"results.date": -1}},
        {"$limit": 1},
        {"$project": {"_id": 0, "date": "$results.date"}}
    ]
    result = list(dbname.get_collection(collection).aggregate(pipeline))
    print(result)
    return result[0]['date'] if result else None
    
    
def insert_data(from_data:str, collection_name:str, start_date:str, end_date:datetime):
    """Permet de remplir une base de donnée jours par jours 100 lignes par 100 ligne

    Args:
        collection_name (str): nom de la collection 
        start_date (str): date de départ (api_service.get_first_date(collection_name))
        end_date (datetime): dernière date dans le dataframe
    """
    step = 100
    print(start_date)
    current_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    
    while current_date <= end_date:
        formatted_date = str(current_date.strftime('%Y-%m-%d'))
        lines_per_date = get_length_per_date(from_data, str(formatted_date))
        print(formatted_date)
        
        for i in range(0, lines_per_date, step):
            rows = min(step, lines_per_date - i)
            try:
                data = fetch_data_by_date(from_data, i, rows, str(formatted_date))
                
                if isinstance(data, list):
                    insert_many_in_coll(collection_name, data)
                else:
                    insert_one_in_coll(collection_name, data)
                    
            except Exception as e:
                print(f"Erreur lors de l'insertion des données pour la date {formatted_date}, offset {i}: {e}")
                print("Réessai dans 5 secondes...")
                time.sleep(5)  
                i -= step  
                continue
                
        current_date += datetime.timedelta(days=1)

def update_data(from_data:str, collection_name:str):
    """Update the data of a collection by looking at the latest date of this collection

    Args:
        collection_name (str): collection name
    """
    insert_data(from_data, collection_name, get_last_date_db(collection_name), get_last_date(from_data))


# Run to update date from eco2mix-regional-tr
#update_data("eco2mix-regional-tr", "eco2mix")

    
