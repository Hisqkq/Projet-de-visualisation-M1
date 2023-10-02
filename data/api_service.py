import requests
import pandas as pd

def fetch_data_to_dataframe():
    url_base = "https://odre.opendatasoft.com/api/records/1.0/search/"
    params = {
        "dataset": "imports-exports-commerciaux",
        "rows": 10000,  # Pour récupérer plus de données, augmentez la valeur de 'rows'
        "sort": "export_france",
    }
    
    response = requests.get(url_base, params=params)
    
    if response.status_code == 200:
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
    
