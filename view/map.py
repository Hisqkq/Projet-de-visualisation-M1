import plotly.express as px

import data.geojson_services as gjs

def build_map(data: dict, homepage: bool=False) -> px.choropleth:
    """Create a map.

    Parameters
    ----------
    data : dict
        Dictionary containing the data.
    homepage : bool
        True if the map is for the homepage, False otherwise, by default False.
    
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
        basemap_visible=False,  # Remove the basemap
    )

    # Update the map
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0}, # Remove margins
        showlegend=False, # Remove the legend
        dragmode=False, # Disable the drag mode
    )
    if not homepage:
        fig.update_layout(geo=dict(bgcolor= '#555555')) # Remove the background color
        fig.update_traces(marker_line_color="#555555", marker_line_width = 1.5) # Add a grey border to the regions"

    return fig

def build_metropolitan_map(homepage=False) -> px.choropleth:
    """Create a metropolitan map (without overseas and Corsica).

    Parameters
    ----------
    homepage : bool
        True if the map is for the homepage, False otherwise.

    Returns
    -------
    px.choropleth
        Figure containing the map.
    
    """
    data = gjs.get_map_data()
    fig = build_map(data, homepage)

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