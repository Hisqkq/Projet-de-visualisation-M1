import configparser
import plotly.graph_objects as go

import data.db_services as dbs
from view.datepicker import default_start_date, default_end_date

### Data ###
# Read the configuration file
config = configparser.ConfigParser()
config.read('data/config.ini')

# Create a dictionary containing the colors for each sector
sector_colors = {sector: config['SectorColorPalette'][sector] for sector in config['SectorColorPalette']}
background_color = str(config['Colors']['background'])
############

def build_pie_chart_production_by_sector(data: list, title: str, background: bool = False) -> go.Figure:
    """Create a pie chart.

    Parameters
    ----------
    data : list
        List containing the data.
    title : str
        Title of the pie chart.
    background : bool
        True if the pie chart has a background, False otherwise.
    
    Returns
    -------
    plotly.graph_objects.Figure
        Figure containing the pie chart.
    
    """
    keys = list(data.keys())
    values = list(data.values())

    def hex_to_rgba(hex, alpha=0.6):
        """Convert hex color to rgba format with specified alpha."""
        hex = hex.lstrip('#')
        return f"rgba({int(hex[0:2], 16)}, {int(hex[2:4], 16)}, {int(hex[4:6], 16)}, {alpha})"

    slice_colors = [sector_colors[key] for key in keys if key in sector_colors]

    slice_colors_transparent = [hex_to_rgba(c) for c in slice_colors]

    fig = go.Figure(data=[
        go.Pie(
            labels=keys, 
            values=values, 
            marker=dict(colors=slice_colors_transparent, line=dict(color=slice_colors, width=2)),
            textfont=dict(color='#FFFFFF')
        )
    ])
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hoverinfo='label+percent',
    )
    fig.update_layout(
        showlegend=False,
        title_text=title,
        title_font_size=14,
        title_font_color="#FFFFFF",
        title_x=0.5,
        paper_bgcolor=background_color,
        font_color="#FFFFFF"
    )
    if not background:
        fig.update_layout(paper_bgcolor=background_color)
        fig.update_layout(font_color="#FFFFFF")
    
    return fig

def metropolitan_pie_chart_production_by_sector(start_date: str = default_start_date,
                                                end_date: str = default_end_date,
                                                is_title: bool = True,
                                                background: bool = False) -> go.Figure:  
    """Create a metropolitan pie chart (without overseas and Corsica).
    
    Parameters
    ----------
    start_date : str, optional
        Starting date, by default default_start_date.
    end_date : str, optional
        Ending date, by default default_end_date.
    is_title : bool, optional
        True if the pie chart has a title, False otherwise, by default True.
    background : bool
        True if the pie chart has a background, False otherwise.
    
    Returns
    -------
    plotly.graph_objects.Figure
        Figure containing the pie chart.
    
    """
    data = dbs.get_mean_for_sectors(
        "DonneesNationales", 
        start_date, end_date, 
        ["eolien", "hydraulique", "nucleaire", "solaire", "fioul", "charbon", "gaz", "bioenergies"]
    )[0]
    title = ''
    if is_title:
        title = "Mix énergétique en Métropole (hors Corse)"
    return build_pie_chart_production_by_sector(data, title, background)

def regional_pie_chart_production_by_sector(region: str, 
                                            start_date: str = default_start_date, 
                                            end_date: str = default_end_date) -> go.Figure:
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
    data = dbs.get_mean_for_sectors(
        "DonneesRegionales", 
        start_date, end_date, 
        ["eolien", "hydraulique", "nucleaire", "solaire", "fioul", "charbon", "gaz", "bioenergies", "thermique"], 
        region
    )[0]
    return build_pie_chart_production_by_sector(data, f"Mix énergétique en {region}")