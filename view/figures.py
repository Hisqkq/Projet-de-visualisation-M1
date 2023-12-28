import plotly.express as px
import configparser

import data.db_services as dbs
from view.datepicker import default_start_date, default_end_date

### Data ###
# Read the configuration file
config = configparser.ConfigParser()
config.read('data/config.ini')

# Create a dictionary containing the colors for each field
field_colors = {field: config['FieldColorPalette'][field] for field in config['FieldColorPalette']}
background_color = str(config['Colors']['background'])
############

## Echanges ##
def build_stacked_bar_chart(arguments: list, 
                            starting_date: str = default_start_date, 
                            ending_date: str = default_end_date) -> px.bar:
    """Create a stacked bar chart.
    
    Parameters
    ----------
    arguments : list
        List of arguments.
    starting_date : str, optional
        Starting date, by default default_start_date.
    ending_date : str, optional
        Ending date, by default default_end_date.
        
    Returns
    -------
    plotly.graph_objects.Figure
        Figure containing the stacked bar chart."""
    # Fetching data and converting JSON to DataFrame
    json_data = dbs.get_data_from_one_date_to_another_date("DonneesNationales", starting_date, ending_date)
    data = dbs.transform_data_to_df(json_data)
    data = dbs.convert_to_numeric(data, arguments)
    
    # Check if the necessary columns are in the DataFrame
    if not all(arg in data.columns for arg in arguments):
        raise ValueError("One or more specified arguments are not in the data")

    # Reshaping the data for stacked bar chart
    data_melted = data.melt(id_vars='date_heure', value_vars=arguments, var_name='category', value_name='value')

    # Creating the stacked bar chart
    fig = px.bar(data_melted, x='date_heure', y='value', color='category', barmode='relative', template="plotly_dark")
    fig.update_layout(bargroupgap=0.01)
    fig.update_layout(paper_bgcolor= background_color)
    fig.update_layout(font_color= "#FFFFFF")
    
    return fig

## Production ##
def build_stacked_area_chart(argument: str = "nucleaire", 
                             starting_date: str = default_start_date, 
                             ending_date: str = default_end_date,
                             homepage:bool=False) -> px.area:
    """Create a stacked area chart.
    
    Parameters
    ----------
    argument : str, optional
        Argument, by default "nucleaire".
    date : str, optional
        Date, by default datetime.datetime.now().strftime("%Y-%m-%d").
    homepage : bool, optional
        True if the stacked area chart is for the homepage, False otherwise, by default False.
        
    Returns
    -------
    plotly.graph_objects.Figure
        Figure containing the stacked area chart."""
    data = dbs.get_data_from_one_date_to_another_date("DonneesRegionales", starting_date, ending_date)
    fig = px.area(data, x="date_heure", y=str(argument), color="libelle_region", title=f"Production {argument}", template="plotly_dark")
    if not homepage:
        fig.update_layout(paper_bgcolor=background_color)
        fig.update_layout(font_color="#FFFFFF") 
    return fig

def build_stacked_area_by_production(starting_date: str = default_start_date, 
                                     ending_date: str = default_end_date,):
    """Create a stacked area chart for each production field.
    
    Parameters
    ----------
    starting_date : str
        Starting date.
    end_date : str
        Ending date.
        
    Returns
    -------
    plotly.graph_objects.Figure
        Figure containing the stacked area chart."""
    data = dbs.transform_data_to_df(dbs.get_data_from_one_date_to_another_date("DonneesNationales", starting_date, ending_date))
    data = data.sort_values(by=['date_heure'])
    data = dbs.remove_nan_from_data(data, "consommation")
    
    production_fields = ["eolien", "hydraulique", "nucleaire", "solaire", "bioenergies", "gaz", "fioul", "charbon"]
    if not set(production_fields).issubset(data.columns):
        missing_fields = list(set(production_fields) - set(data.columns))
        raise ValueError(f"Les colonnes suivantes sont manquantes dans le DataFrame: {missing_fields}")

    fig = px.area(data, x="date_heure", y=production_fields, title="Production par filière", color_discrete_map=field_colors, template="plotly_dark")
    fig.update_layout(paper_bgcolor=background_color)
    fig.update_layout(font_color="#FFFFFF") 
    return fig

## Consommation ##
def build_line_chart_with_prediction(starting_date: str = default_start_date, 
                                     ending_date: str = default_end_date, 
                                     homepage:bool=False) -> px.area:
    """Create a line chart.
    
    Parameters
    ----------
    starting_date : str, optional
        Starting date, by default default_start_date.
    ending_date : str, optional
        Ending date, by default default_end_date.
    homepage : bool, optional
        True if the line chart is for the homepage, False otherwise, by default False.
        
    Returns
    -------
    plotly.graph_objects.Figure
        Figure containing the line chart.
    """
    # Fetching data and converting JSON to DataFrame
    json_data = dbs.get_data_from_one_date_to_another_date("DonneesNationales", starting_date, ending_date)
    data = dbs.transform_data_to_df(json_data)
    #Order data by datetime
    data = data.sort_values(by=['date_heure'])
    data = dbs.remove_nan_from_data(data, "consommation")

    # Check if the necessary columns are in the DataFrame
    if not {'date_heure', 'consommation', 'prevision_j', 'prevision_j1'}.issubset(data.columns):
        raise ValueError("One or more required columns are missing in the data")

    # Creating the line chart
    line_chart_cons = px.area(data, x="date_heure", y="consommation", template="plotly_dark")
    line_chart_cons.add_scatter(x=data["date_heure"], y=data["prevision_j"], mode='lines', name='Prediction J')
    line_chart_cons.add_scatter(x=data["date_heure"], y=data["prevision_j1"], mode='lines', name='Prediction J-1')
    line_chart_cons.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        xanchor="center",
        y = 1.2,
        x = 0.5
    ))

    if not homepage:
        line_chart_cons.update_layout(paper_bgcolor=background_color)
        line_chart_cons.update_layout(font_color="#FFFFFF")

    return line_chart_cons

def build_line_chart_consommation_by_region(starting_date: str = default_start_date, 
                                            ending_date: str = default_end_date, 
                                            homepage:bool=False) -> px.line:
    """Create a line chart.
    
    Parameters
    ----------
    starting_date : str, optional
        Starting date, by default default_start_date.
    ending_date : str, optional
        Ending date, by default default_end_date.
    homepage : bool, optional
        True if the line chart is for the homepage, False otherwise, by default False.
        
    Returns
    -------
    plotly.graph_objects.Figure
        Figure containing the line chart.
    """
    # Fetching data and converting JSON to DataFrame
    json_data = dbs.get_data_from_one_date_to_another_date("DonneesRegionales", starting_date, ending_date)
    data = dbs.transform_data_to_df(json_data)
    #Order data by datetime
    data = data.sort_values(by=['date_heure'])
    data = dbs.remove_nan_from_data(data, "consommation")

    # Check if the necessary columns are in the DataFrame
    if not {'date_heure', 'consommation', 'libelle_region'}.issubset(data.columns):
        raise ValueError("One or more required columns are missing in the data")

    # Creating the line chart
    line_chart_cons = px.line(data, x="date_heure", y="consommation", color="libelle_region", template="plotly_dark")
    line_chart_cons.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        xanchor="center",
        y = 1.2,
        x = 0.5
    ))

    if not homepage:
        line_chart_cons.update_layout(paper_bgcolor=background_color)
        line_chart_cons.update_layout(font_color="#FFFFFF")

    return line_chart_cons