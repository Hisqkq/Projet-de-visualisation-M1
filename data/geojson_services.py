import json
import pandas as pd
import configparser

config = configparser.ConfigParser()
config.read('data/config.ini')

JSON = config.get('GeoJSON', 'json')

def get_json(path: str = JSON) -> dict:
    """Load a JSON file.

    Parameters
    ----------
    path : str
        Path to the JSON file.
    
    Returns
    -------
    dict
        Dictionary containing the data.
    
    """
    with open(path) as JSON_file:
        return json.load(JSON_file)

def exclude_overseas_and_corsica(data: dict) -> dict:
    """Exclude the overseas and Corsica from the data.

    Parameters
    ----------
    data : dict
        Dictionary containing the data.
    
    Returns
    -------
    dict
        Dictionary containing the regions without the overseas and Corsica.
    
    """
    codes_out = ["01", "02", "03", "04", "06", "94"]
    data['features'] = [f for f in data['features'] if f['properties']['code'] not in codes_out]
    return data

def get_map_data() -> dict:
    """Get the data for the map.

    Returns
    -------
    dict
        Dictionary containing the data.
    
    """
    data = get_json()
    data = exclude_overseas_and_corsica(data)
    return data

def get_region_map_data(region: str) -> dict:
    """Get the data for the map of a specific region.

    Parameters
    ----------
    region : str
        Name of the region.
    
    Returns
    -------
    dict
        Dictionary containing the data.
    
    """
    data = get_json()
    data = [f for f in data['features'] if f['properties']['nom'] == region][0]
    return data

def create_df(data: dict) -> pd.DataFrame:
    """Create a DataFrame from the data to use it in a choropleth map (Plotly).

    Parameters
    ----------
    data : dict
        Dictionary containing the data.
    
    Returns
    -------
    pd.DataFrame
        DataFrame containing the data.
    
    """
    if 'features' not in data: # If the data is for a specific region
        return pd.DataFrame({'code': data['properties']['code'], 'nom': data['properties']['nom'], 'geometry': data['geometry']})

    tab = {'code': [], 'nom': [], 'geometry': []}
    for f in data['features']:
        tab['code'].append(f['properties']['code'])
        tab['nom'].append(f['properties']['nom'])
        tab['geometry'].append(f['geometry'])
    return pd.DataFrame(tab)