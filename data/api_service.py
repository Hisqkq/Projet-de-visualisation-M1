import requests
import pandas as pd

def fetch_data_to_dataframe(datasetID, sort = "", rows = 10000):
    url_base = "https://odre.opendatasoft.com/api/records/1.0/search/"
    params = {
        "dataset": datasetID,
        "rows": rows,  # Pour récupérer plus de données, augmentez la valeur de 'rows'
        "sort": sort,
    }
    
    response = requests.get(url_base, params=params)
    
    if response.status_code == requests.codes.ok:
        data = response.json()
        records = data.get('records', [])
        
        data_list = [record.get('fields', {}) for record in records]
        
        dataframe = pd.DataFrame(data_list)
        
        return dataframe
    else:
        print(f"Échec de la requête: {response.status_code}")
        print(response.text)
        return pd.DataFrame()  



def fetch_data_consommation_quotidienne_brute():
    url = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/consommation-quotidienne-brute-regionale/records"
    params = {
        "select": "sum(consommation_brute_electricite_rte) as somme_consommation_elec, region",
        "group_by": "region"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        
        # Conversion des résultats en DataFrame
        dataframe = pd.DataFrame(results)
        print(dataframe)
        return dataframe
    else:
        print(f"Échec de la requête: {response.status_code}")
        print(response.text)
        return pd.DataFrame()
    
def json_data_consommation_quotidienne_brute():
    url = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/consommation-quotidienne-brute-regionale/records"
    params = {
        "select": "sum(consommation_brute_electricite_rte) as somme_consommation_elec, region",
        "group_by": "region"
    }

    response = requests.get(url, params=params)
    data=[{}]
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Échec de la requête: {response.status_code}")
        print(response.text)
        return data
    
def fetch_eco2mix(start, rows, date):
    url = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-regional-tr/records"
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
        return data.get('total_count')[0]
    else:
        print(f"Échec de la requête: {response.status_code}")
        print(response.text)
        return
    

print(get_first_date("eco2mix-regional-tr") )
