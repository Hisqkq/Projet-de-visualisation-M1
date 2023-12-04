import requests
import mongodb
import datetime
import time

## CONNECT TO DB
dbname = mongodb.get_database()
    
###### API ######     

URL = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/"

def fetch_data_by_date(data:str, start:int, rows:int, date:str):
    """Fetch data from a dataset by date and offset
    
    Args:
        dataset (str): dataset name
        start (int): offset
        rows (int): number of rows desired
        date (str): date
    Returns:
        JSON: data
    """
    url = f"{URL}{data}" + "/records"
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
    
def get_date(data:str, first:bool=True):
    """get the minimum date in a dataset

    Args:
        dataset (str): _description_
        first (bool): True to get first date, False to get last date
    Returns:
        _type_: _description_
    """

    if first: date = "date"
    else: date = "-date"

    url = f"{URL}{data}" + "/records"
    params = {
        "select": "date",
        "rows": 1,
        "order_by": date,
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
    
def get_length_per_date(data:str, date:str):
    """get the minimum date in a dataset

    Args:
        dataset (str): _description_

    Returns:
        _type_: _description_
    """
    url = f"{URL}{data}" + "/records"
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
    
def insert_in_coll(table_name:str, data:dict):
    """Add data (JSON) to a collection

    Args:
        table_name (str): nom de la table visée
        data (dict): données à injecter
    """
    if isinstance(data, list): 
        dbname.get_collection(table_name).insert_many(data)
        return
    else: dbname.get_collection(table_name).insert_one(data)
    
def get_last_date_db(collection):
    """Get the last date in a collection
    
    Args:
        collection (str): name of the collection
    Returns:
        str : date
    """
    pipeline = [
        {"$unwind": "$results"},
        {"$sort": {"results.date": -1}},
        {"$limit": 1},
        {"$project": {"_id": 0, "date": "$results.date"}}
    ]
    result = list(dbname.get_collection(collection).aggregate(pipeline))
    return result[0]['date'] if result else None
    
def delete_data_last_date(collection):
    """Delete data from the last date in a collection
    
    Args:
        collection (str): name of the collection
    """
    last_date = get_last_date_db(collection)
    dbname.get_collection(collection).delete_many({"results.date": last_date})
    
def update_data(from_data:str, collection_name:str):
    """Allows to update a collection with new data 100 rows by 100

    Args:
        from_data (str): nom de la dataset API
        collection_name (str): nom de la collection 
    """
    step = 100

    if not list(dbname[collection_name].find()):
        start_date = get_date(from_data)
    else: 
        start_date = get_last_date_db(collection_name)
        delete_data_last_date(collection_name) # delete data from last date in collection to avoid duplicates when updating data

    end_date = get_date(from_data, first = False)
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
                insert_in_coll(collection_name, data)
                    
            except Exception as e:
                print(f"Erreur lors de l'insertion des données pour la date {formatted_date}, offset {i}: {e}")
                print("Réessai dans 5 secondes...")
                time.sleep(5)  
                i -= step  
                continue
                
        current_date += datetime.timedelta(days=1)


# Run to update date from eco2mix-regional-tr
#update_data("eco2mix-regional-tr", "eco2mix")

    
