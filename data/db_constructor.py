import configparser
import data.mongodb as mongodb
import datetime
import requests
import time
import concurrent.futures
import calendar
from pymongo import ASCENDING

config = configparser.ConfigParser()
config.read("data/config.ini")

## CONNECT TO DB
dbname = mongodb.get_database()

###### API ######

URL = config.get("API", "url")


def fetch_data_by_date(data: str, start: int, rows: int, date: str) -> dict:
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
    params = {"offset": start, "rows": rows, "where": f"date='{date}'"}
    response = requests.get(url, params=params)
    data = [{}]
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Échec de la requête: {response.status_code}")
        print(response.text)
        return


def get_date(data: str, first: bool = True) -> str:
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
    params = {
        "select": "date",
        "rows": 1,
        "order_by": date,
    }
    response = requests.get(url, params=params)
    data = [{}]
    if response.status_code == 200:
        data = response.json()
        return data.get("results")[0]["date"]
    else:
        print(f"Échec de la requête: {response.status_code}")
        print(response.text)
        return


def get_length_per_date(data: str, date: str) -> int:
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
    params = {"select": "date", "rows": 1, "where": f"date='{date}'"}
    response = requests.get(url, params=params)
    data = [{}]
    if response.status_code == 200:
        data = response.json()
        return data.get("total_count")
    else:
        print(f"Échec de la requête: {response.status_code}")
        print(response.text)
        return


###### Construction ######


def create_collection(name: str) -> None:
    """Create a collection in the database

    Parameters
    ----------
    name : str
        Name of the collection.
    """
    if not (name in dbname.list_collection_names()):
        dbname.create_collection(name)


def insert_in_coll(table_name: str, data: dict) -> None:
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
    else:
        dbname.get_collection(table_name).insert_one(data)


def get_last_date_db(collection: str) -> str:
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
        {
            "$unwind": "$results"
        },
        {
            "$sort": {
                "results.date": -1
            }
        },
        {
            "$limit": 1
        },
        {
            "$project": {
                "_id": 0,
                "date": "$results.date"
            }
        },
    ]
    result = list(dbname.get_collection(collection).aggregate(pipeline))
    return result[0]["date"] if result else None


def delete_data_last_date(collection: str) -> None:
    """Delete today's data in a collection

    Parameters
    ----------
    collection : str
        Name of the collection.
    """
    start_date = datetime.datetime.now() - datetime.timedelta(days=3)
    dbname.get_collection(collection).delete_many(
        {"results.date": {
            "$gte": start_date.strftime("%Y-%m-%d")
        }})


def update_data_for_month(from_data: str, collection_name: str, year: int, month: int) -> None:
    """Update data in a collection for a specific month

    Parameters
    ----------
    from_data : str
        Name of the dataset.
    collection_name : str
        Name of the collection.
    year : int
        Year to update.
    month : int
        Month to update.
    """
    step = 100
    _, days_in_month = calendar.monthrange(year, month)
    
    for day in range(1, days_in_month + 1):
        current_date = datetime.date(year, month, day)
        formatted_date = current_date.strftime("%Y-%m-%d")
        lines_per_date = get_length_per_date(from_data, formatted_date)

        for i in range(0, lines_per_date, step):
            rows = min(step, lines_per_date - i)
            try:
                data = fetch_data_by_date(from_data, i, rows, formatted_date)
                insert_in_coll(collection_name, data)
            except Exception as e:
                print(f"Erreur lors de l'insertion des données pour la date {formatted_date}, offset {i}: {e}")
                print("Réessai dans 5 secondes...")
                time.sleep(5)
                i -= step
                continue

def update_data(from_data: str, collection_name: str) -> None:
    """Update data in a collection using multithreading

    Parameters
    ----------
    from_data : str
        Name of the dataset.
    collection_name : str
        Name of the collection.
    """
    if not list(dbname[collection_name].find()):
        start_date = datetime.datetime.strptime(get_date(from_data), "%Y-%m-%d")
    else:
        start_date = datetime.datetime.strptime(get_last_date_db(collection_name), "%Y-%m-%d")
        if start_date >= datetime.datetime.now():
            start_date = datetime.datetime.now() - datetime.timedelta(days=3)
        delete_data_last_date(collection_name)

    end_date = datetime.datetime.strptime(get_date(from_data, first=False), "%Y-%m-%d")

    months_to_process = []
    current_date = start_date.replace(day=1)
    while current_date <= end_date:
        months_to_process.append((current_date.year, current_date.month))
        current_date += datetime.timedelta(days=32)
        current_date = current_date.replace(day=1)

    # Use multithreading to update data
    with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
        futures = [executor.submit(update_data_for_month, from_data, collection_name, year, month) 
                   for year, month in months_to_process]
        concurrent.futures.wait(futures)

def create_indexes() -> None:
    """Create indexes for the collections to optimize query performance"""
    
    # Index for DonneesNationales
    national_collection = dbname["DonneesNationales"]
    national_collection.create_index([("results.date", ASCENDING)], background=True)
    print("Index created for DonneesNationales on date")

    # Index for DonneesRegionales
    regional_collection = dbname["DonneesRegionales"]
    regional_collection.create_index([("results.date", ASCENDING)], background=True)
    regional_collection.create_index([("results.region", ASCENDING)], background=True)
    regional_collection.create_index([
        ("results.date", ASCENDING),
        ("results.region", ASCENDING)
    ], background=True)
    print("Indexes created for DonneesRegionales on date and region")

def perform_update():
    """Update data in the database using multithreading and create indexes"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = [
            executor.submit(update_data, "eco2mix-national-cons-def", "DonneesNationales"),
            executor.submit(update_data, "eco2mix-regional-cons-def", "DonneesNationales"),
            executor.submit(update_data, "eco2mix-national-tr", "DonneesNationales"),
            executor.submit(update_data, "eco2mix-regional-tr", "DonneesRegionales")
        ]
        concurrent.futures.wait(futures)
    
    create_indexes()
