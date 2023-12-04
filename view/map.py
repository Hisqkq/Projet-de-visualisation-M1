import plotly.express as px

import data.geojson_services as gjs

def build_map(data: dict) -> px.choropleth:
    """Create a map.

    Parameters
    ----------
    data : dict
        Dictionary containing the data.
    
    Returns
    -------
    px.choropleth
        Figure containing the map.
    
    """
    # Create a DataFrame for the map
    df = gjs.create_df(data)

    # Create a choropleth map
    fig = px.choropleth(
        df, # DataFrame containing the map data
        geojson=data,  # Use the GeoJSON
        featureidkey="properties.nom",  # Key identifying the region in the GeoJSON
        locations="nom",  # Column in the DataFrame corresponding to the regions
        color="code",  # Column in the DataFrame corresponding to the values for the coloration
        color_continuous_scale="Viridis",  # Scale of colors
        fitbounds="locations",  # Fit the map to the regions
        basemap_visible=False  # Remove the basemap
    )

    # Update the map
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0}, # Remove margins
        showlegend=False, # Remove the legend
        dragmode=False # Disable the drag mode
    )

    return fig

def build_metropolitan_map() -> px.choropleth:
    """Create a metropolitan map (without overseas and Corsica).

    Returns
    -------
    px.choropleth
        Figure containing the map.
    
    """
    data = gjs.get_map_data()
    fig = build_map(data)

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

    return fig