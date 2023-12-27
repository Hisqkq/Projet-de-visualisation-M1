import plotly.express as px
import configparser

import data.geojson_services as gjs

### Data ###
# Read the configuration file
config = configparser.ConfigParser()
config.read('data/config.ini')

background_color = str(config['Colors']['background'])
token = str(config['Mapbox']['mapbox_token'])
############

px.set_mapbox_access_token(token)

def build_map(data: dict, background: bool=False) -> px.choropleth:
    """Create a map.

    Parameters
    ----------
    data : dict
        Dictionary containing the data.
    background : bool
        True if the map has a background, False otherwise.
    
    Returns
    -------
    px.choropleth
        Figure containing the map.
    
    """
    # Create a DataFrame for the map
    df = gjs.create_df(data) # Dataframe for the map
    
    center_lat, center_lon = gjs.calculate_centroid(data) # Calculate the centroid of the map
    
    # Create a choropleth map
    fig = px.choropleth_mapbox(
        df,  
        geojson=data, # Geojson data
        featureidkey="properties.nom", # Key to match the data
        locations="nom", # Column containing the names of the regions
        color="code", # Column containing the color of the regions
        color_discrete_sequence=["#ADD8E6"], # Color of the regions (light blue)
        mapbox_style="mapbox://styles/tlavandier/clqmy8zxa00qt01o3ax462t6g", # Without background
        #mapbox_style="mapbox://styles/tlavandier/clqmwyr7w00qr01o33d8g5ien", # With background
        zoom=4, 
        center={"lat": center_lat, "lon": center_lon},
        opacity=0.8,
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    if not background: # Wondering if it's useful now
        fig.update_layout(geo=dict(bgcolor= 'black'), paper_bgcolor= 'rgba(0,0,0,0)')
        fig.update_traces(marker_line_color="#21222b", marker_line_width = 1.5) 
    
    fig.update_traces(
        marker_line_color="#4169E1", # Color of the border of the regions
        marker_line_width=1.5, 
        marker_opacity=0.8 
    )
    fig.update_layout(dragmode=False, # Dragmode doesn't work :/
                      showlegend=False)

    return fig

def build_metropolitan_map(background=False) -> px.choropleth:
    """Create a metropolitan map (without overseas and Corsica).

    Parameters
    ----------
    background : bool
        True if the map has a background, False otherwise.

    Returns
    -------
    px.choropleth
        Figure containing the map.
    
    """
    data = gjs.get_map_data()
    fig = build_map(data, background)

    return fig

def build_region_map(region: str) -> px.choropleth:
    """Create a map for a specific region.
    
    Parameters
    ----------
    region : str
        Name of the region.
    
    Returns
    -------
    px.choropleth
        Figure containing the map.
    
    """
    data = gjs.get_region_map_data(region)
    fig = build_map(data)
    fig.update_layout(
            mapbox={"zoom": 5.5} # Zoom on the selected region
        )

    return fig