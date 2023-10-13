import requests

def fetch_data(datasetID, rows = 100, sort = ""):
    url = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/"
    url += datasetID + "/records"
    params = {
        "rows": rows,
        "sort": sort
    }
    response = requests.get(url, params=params)
    data=[{}]
    if response.status_code == requests.codes.ok:
        data = response.json()
        return data
    else:
        print(f"Échec de la requête: {response.status_code}")
        print(response.text)
        return data