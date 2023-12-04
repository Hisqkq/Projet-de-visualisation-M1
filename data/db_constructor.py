import requests
import mongodb
import datetime
import time
import configparser

config = configparser.ConfigParser()
config.read('data/config.ini')

## CONNECT TO DB
dbname = mongodb.get_database()
    
###### API ######   
  
URL = config.get('API', 'url')

def fetch_data_by_date(data:str, start:int, rows:int, date:str):
    """Fetch data from a dataset by date and offset
    
    Parameters
    ----------
    data : str
        Name of the dataset.
    start : int
        Offset.
    rows : int
        Number of rows.
    date : str
        Date of the data.

    Returns
    -------
    dict
        Dictionary containing the data. 
    """
    url = f"{URL}{data}" + "/records"
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
    """Get the minimum or maximum date in a dataset

    Parameters
    ----------
    data : str
        Name of the dataset.
    first : bool, optional
        If True, get the minimum date, else get the maximum date. The default is True.
    
    Returns
    -------
    str
        Date.
    """

    date = "date" if first else "-date"

    url = f"{URL}{data}" + "/records"
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
    """Get the number of rows for a given date

    Parameters
    ----------
    data : str
        Name of the dataset.
    date : str
        Date of the data.

    Returns
    -------
    int
        Number of rows.
    """
    url = f"{URL}{data}" + "/records"
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
    """Create a collection in the database

    Parameters
    ----------
    name : str
        Name of the collection.
    """
    if(not (name in dbname.list_collection_names())):
        dbname.create_collection(name)    
    
def insert_in_coll(table_name:str, data:dict):
    """Insert data in a collection (JSON)

    Parameters
    ----------
    table_name : str
        Name of the collection.
    data : dict
        Data to insert.
    """
    if isinstance(data, list): 
        dbname.get_collection(table_name).insert_many(data)
        return
    else: dbname.get_collection(table_name).insert_one(data)
    
def get_last_date_db(collection):
    """Get the last date in a collection
    
    Parameters
    ----------
    collection : str
        Name of the collection.

    Returns
    -------
    str
        Date.
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
    
    Parameters
    ----------
    collection : str
        Name of the collection.
    """
    last_date = get_last_date_db(collection)
    dbname.get_collection(collection).delete_many({"results.date": last_date})
    
def update_data(from_data:str, collection_name:str):
    """Update data in a collection

    Parameters
    ----------
    from_data : str
        Name of the dataset.
    collection_name : str
        Name of the collection.
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
