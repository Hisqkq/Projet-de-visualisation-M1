import plotly.express as px
import json
import pandas as pd

JSON = './data/regions.geojson'

def get_json(path: str = JSON) -> dict:
    """Load a JSON file.
    :param path: Path to the JSON file.
    :return: Dictionary containing the JSON file.
    """
    with open(path) as JSON_file:
        return json.load(JSON_file)

def exclude_overseas_and_corsica(data: dict) -> dict:
    """Filter the metropolitan regions from the data.
    :param data: Dictionary containing the data.
    :return: Dictionary containing the metropolitan regions.
    """
    codes_out = ["01", "02", "03", "04", "06", "94"]
    data['features'] = [f for f in data['features'] if f['properties']['code'] not in codes_out]
    return data

def build_metropolitan_map(data: dict) -> px.choropleth:
    """Create a metropolitan map.
    :param data: Dictionary containing the data.
    :return: Figure containing the map.
    """
    features = data['features']
    tab = {'code': [], 'nom': [], 'geometry': []}

    for feature in features:
        tab['code'].append(feature['properties']['code'])
        tab['nom'].append(feature['properties']['nom'])
        tab['geometry'].append(feature['geometry'])

    df = pd.DataFrame(tab) # Create a DataFrame with the map data

    # Create a choropleth map
    fig = px.choropleth(df, 
                        geojson=data,  # Use the GeoJSON
                        featureidkey="properties.nom",  # Key identifying the region in the GeoJSON
                        locations="nom",  # Column in the DataFrame corresponding to the regions
                        color="code",  # Column in the DataFrame corresponding to the values for the coloration
                        color_continuous_scale="Viridis",  # Scale of colors
                        title="Carte des régions de France")

    # Update the map
    fig.update_geos(fitbounds="locations", visible=False) # Fit the map to the regions
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) # Remove margins
    fig.update_layout(showlegend=False) # Remove the legend
    fig.update_layout(dragmode=False) # Disable the drag mode
    
    return fig

def build_region_map(data: dict, region: str) -> px.choropleth:
    """Create a map for a specific region.
    :param data: Dictionary containing the data.
    :param region: Region to display.
    :return: Figure containing the map.
    """
    data = [f for f in data['features'] if f['properties']['nom'] == region][0]
    tab = {'code': data['properties']['code'], 'nom': data['properties']['nom'], 'geometry': data['geometry']}

    df = pd.DataFrame(tab) # Create a DataFrame with the map data

    # Create a choropleth map
    fig = px.choropleth(df, 
                        geojson=data,  # Use the GeoJSON
                        featureidkey="properties.nom",  # Key identifying the region in the GeoJSON
                        locations="nom",  # Column in the DataFrame corresponding to the regions
                        color="code",  # Column in the DataFrame corresponding to the values for the coloration
                        color_continuous_scale="Viridis",  # Scale of colors
                        title="Carte des régions de France")

    # Update the map
    fig.update_geos(fitbounds="locations", visible=False) # Fit the map to the regions
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}) # Remove margins
    fig.update_layout(showlegend=False) # Remove the legend
    fig.update_layout(dragmode=False) # Disable the drag mode

    return fig