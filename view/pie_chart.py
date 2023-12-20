import plotly.express as px

import data.db_services as dbs
from view.datepicker import default_start_date, default_end_date

def build_pie_chart_production_by_field(data: list, title: str) -> px.pie:
    """Create a pie chart.

    Parameters
    ----------
    data : list
        List containing the data.
    title : str
        Title of the pie chart.
    
    Returns
    -------
    plotly.graph_objects.Figure
        Figure containing the pie chart.
    """
    fig = px.pie(names=list(data.keys()), values=list(data.values()), title=title)
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hoverinfo='label+percent',
        marker=dict(
            colors=px.colors.qualitative.Pastel1,
            line=dict(color='#FFFFFF', width=2)
        )
    )
    fig.update_layout(
        showlegend=False,
        title=dict(
            font=dict(size=24)
        )
    )
    return fig

def build_metropolitan_pie_chart_production_by_field(start_date: str = default_start_date,
                                                     end_date: str = default_end_date) -> px.pie:  
    """Create a metropolitan pie chart (without overseas and Corsica).
    
    Parameters
    ----------
    start_date : str, optional
        Starting date, by default default_start_date.
    end_date : str, optional
        Ending date, by default default_end_date.
    
    Returns
    -------
    plotly.graph_objects.Figure
        Figure containing the pie chart.
    """
    data = dbs.get_mean_for_fields(
        "DonneesNationales", 
        start_date, end_date, 
        ["eolien", "hydraulique", "nucleaire", "solaire", "fioul", "charbon", "gaz", "bioenergies"]
    )[0]
    return build_pie_chart_production_by_field(data, "Répartition de la Production des Sources d’Énergie en Métropole (hors Corse)")

def build_region_pie_chart_production_by_field(region: str, 
                                               start_date: str = default_start_date, 
                                               end_date: str = default_end_date) -> px.pie:
    """Create a pie chart for a specific region.

    Parameters
    ----------
    region : str
        Region.
    start_date : str, optional
        Starting date, by default default_start_date.
    end_date : str, optional
        Ending date, by default default_end_date.
    
    Returns
    -------
    plotly.graph_objects.Figure
        Figure containing the pie chart.
    """
    data = dbs.get_mean_for_fields_in_a_region(
        "DonneesRegionales", 
        start_date, end_date, 
        ["eolien", "hydraulique", "nucleaire", "solaire", "fioul", "charbon", "gaz", "bioenergies"], 
        region
    )[0]
    return build_pie_chart_production_by_field(data, f"Répartition de la Production des Sources d’Énergie en {region}")