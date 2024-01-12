import configparser
import plotly.express as px

import data.db_services as dbs
import data.geojson_services as gjs

### Data ###
# Read the configuration file
config = configparser.ConfigParser()
config.read('data/config.ini')

background_color = str(config['Colors']['background'])
token = str(config['Mapbox']['mapbox_token'])
############

px.set_mapbox_access_token(token)


def build_map(data: dict, background: bool = False) -> px.choropleth:
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
    df = gjs.create_df(data)  # Dataframe for the map

    center_lat, center_lon = gjs.calculate_centroid(
        data)  # Calculate the centroid of the map

    # Create a choropleth map
    fig = px.choropleth_mapbox(
        df,
        geojson=data,  # Geojson data
        featureidkey="properties.nom",  # Key to match the data
        locations="nom",  # Column containing the names of the regions
        color="code",  # Column containing the color of the regions
        color_discrete_sequence=["#ADD8E6"
                                 ],  # Color of the regions (light blue)
        mapbox_style=
        "mapbox://styles/tlavandier/clqmy8zxa00qt01o3ax462t6g",  # Without background
        zoom=4,
        center={
            "lat": center_lat,
            "lon": center_lon
        },
        opacity=0.8,
    )
    fig.update_layout(margin={
        "r": 0,
        "t": 0,
        "l": 0,
        "b": 0
    },
                      showlegend=False)

    if not background:
        fig.update_layout(geo=dict(bgcolor='black'),
                          paper_bgcolor='rgba(0,0,0,0)')
        fig.update_traces(marker_line_color="#21222b", marker_line_width=1.5)

    fig.update_traces(
        marker_line_color="#4169E1",  # Color of the border of the regions
        marker_line_width=1.5,
        marker_opacity=0.8)

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
    fig.update_layout(mapbox={"zoom": 5.5}  # Zoom on the selected region
                      )

    return fig


def build_map_colors(starting_date: str,
                     ending_date: str) -> px.choropleth_mapbox:
    """Create a map with colors.

    Parameters
    ----------
    starting_date : str
        Starting date.
    ending_date : str
        Ending date.
    
    Returns
    -------
    px.choropleth
        Figure containing the map.
    
    """
    data = gjs.get_map_data()
    df = gjs.create_df(data)

    mean_cons = dbs.get_mean_consommation_by_region(starting_date, ending_date)

    cons_df = gjs.color_df(mean_cons)  # Dataframe for the colors

    df = df.merge(cons_df, left_on='nom', right_on='region')

    fig = px.choropleth_mapbox(
        df,
        geojson=data,
        featureidkey="properties.nom",
        locations="nom",
        color="mean_consommation",
        color_continuous_scale="Blues",
        range_color=(df['mean_consommation'].min(),
                     df['mean_consommation'].max()),
        mapbox_style="mapbox://styles/tlavandier/clqmy8zxa00qt01o3ax462t6g",
        zoom=4,
        center={
            "lat": 46.2276,
            "lon": 2.2137
        },
        opacity=0.5,
    )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_traces(marker_line_width=0, marker_opacity=0.8)
    fig.update_layout(coloraxis_colorbar=dict(
        title="Consommation Moyenne (MW)",
        thicknessmode="pixels",
        thickness=15,
        lenmode="pixels",
        len=300,
        yanchor="top",
        y=1,
        ticks="outside",
        ticksuffix=" MW",
        dtick=5000,
        bgcolor='rgba(0,0,0,0)',
        titlefont=dict(color='white'),
        tickfont=dict(color='white'),
    ),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')

    return fig


def build_map_animation() -> px.choropleth_mapbox:
    """Create a map animation for the renewable energy production.

    Parameters
    ----------
    starting_date : str
        Starting date.
    ending_date : str
        Ending date.
    
    Returns
    -------
    px.choropleth
        Figure containing the map.
    
    """
    data = gjs.get_map_data()
    df = gjs.create_df(data)

    mean_renewable_prod = dbs.get_mean_renewable_production_by_year()

    df = df.merge(mean_renewable_prod, left_on='nom', right_on='region')

    fig = px.choropleth_mapbox(
        df,
        geojson=data,
        featureidkey="properties.nom",
        locations="nom",
        color="moyenne_renouvelable",
        color_continuous_scale="Greens",
        range_color=(df['moyenne_renouvelable'].min(),
                     df['moyenne_renouvelable'].max()),
        mapbox_style="mapbox://styles/tlavandier/clqmy8zxa00qt01o3ax462t6g",
        zoom=3.8,
        center={
            "lat": 46.2276,
            "lon": 2.2137
        },
        opacity=0.5,
        animation_frame="annee",
        animation_group="region",
    )

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_traces(marker_line_width=0, marker_opacity=0.8)
    fig.update_layout(coloraxis_colorbar=dict(
        title="Production moyenne (MW)",
        thicknessmode="pixels",
        thickness=15,
        lenmode="pixels",
        len=300,
        yanchor="top",
        y=1,
        ticks="outside",
        ticksuffix=" MW",
        dtick=5000,
        bgcolor='rgba(0,0,0,0)',
        titlefont=dict(color='white'),
        tickfont=dict(color='white'),
    ),
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')

    return fig
