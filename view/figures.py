import plotly.express as px
import plotly.graph_objects as go

import data.db_services as dbs
from view.datepicker import default_start_date, default_end_date
import configparser

config = configparser.ConfigParser()
config.read('data/config.ini')

field_colors = {field: config['FieldColorPalette'][field] for field in config['FieldColorPalette']}

def build_line_chart_with_prediction(starting_date: str = default_start_date, 
                                     ending_date: str = default_end_date) -> px.area:
    """Create a line chart.
    
    Parameters
    ----------
    starting_date : str, optional
        Starting date, by default default_start_date.
    ending_date : str, optional
        Ending date, by default default_end_date.
        
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
    line_chart_cons = px.area(data, x="date_heure", y="consommation")
    line_chart_cons.add_scatter(x=data["date_heure"], y=data["prevision_j"], mode='lines', name='Prediction J')
    line_chart_cons.add_scatter(x=data["date_heure"], y=data["prevision_j1"], mode='lines', name='Prediction J-1')

    return line_chart_cons


def build_pie_chart_production_by_field(start_date: str = default_start_date, 
                                        end_date: str = default_end_date, legend = True) -> px.pie:
    """Create a pie chart.

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

    # Récupération des données moyennes
    data = dbs.get_mean_by_date_from_one_date_to_another_date("DonneesNationales", start_date, end_date, ["eolien", "hydraulique", "nucleaire", "solaire", "fioul", "charbon", "gaz", "bioenergies"])[0]

    # Extraction des clés et des valeurs pour le diagramme circulaire
    keys = list(data.keys())
    values = list(data.values())

    # Création d'une liste de couleurs pour les tranches du diagramme circulaire, en utilisant field_colors
    slice_colors = [field_colors[key] for key in keys if key in field_colors]

    # Création du diagramme circulaire avec Graph Objects
    fig = go.Figure(data=[go.Pie(labels=keys, values=values, marker=dict(colors=slice_colors))])

    # Mise à jour des traces pour le positionnement du texte et les informations au survol
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hoverinfo='label+percent',
    )

    # Mise à jour de la mise en page pour ajuster le titre
    fig.update_layout(
        showlegend=False if legend == False else True,
        title_text='Répartition de la Production des Sources d’Énergie',
        title_font_size=24
    )

    return fig



def build_stacked_area_chart(argument: str = "nucleaire", 
                             starting_date: str = default_start_date, 
                             ending_date: str = default_end_date) -> px.area:
    """Create a stacked area chart.
    
    Parameters
    ----------
    argument : str, optional
        Argument, by default "nucleaire".
    date : str, optional
        Date, by default datetime.datetime.now().strftime("%Y-%m-%d").
        
    Returns
    -------
    plotly.graph_objects.Figure
        Figure containing the stacked area chart."""
    data = dbs.get_data_from_one_date_to_another_date("DonneesRegionales", starting_date, ending_date)
    return px.area(data, x="date_heure", y=str(argument), color="libelle_region", title=f"Production {argument}")


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
    fig = px.bar(data_melted, x='date_heure', y='value', color='category', barmode='relative')
    fig.update_layout(bargroupgap=0.01)
    fig.update_traces(marker_line_width=0) 
    
    return fig


def build_stacked_area_by_production(starting_date, end_date):
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
    data = dbs.transform_data_to_df(dbs.get_data_from_one_date_to_another_date("DonneesNationales", starting_date, end_date))
    data = data.sort_values(by=['date_heure'])
    data = dbs.remove_nan_from_data(data, "consommation")
    
    production_fields = ["eolien", "hydraulique", "nucleaire", "solaire", "bioenergies", "gaz", "fioul", "charbon"]
    if not set(production_fields).issubset(data.columns):
        missing_fields = list(set(production_fields) - set(data.columns))
        raise ValueError(f"Les colonnes suivantes sont manquantes dans le DataFrame: {missing_fields}")

    return px.area(data, x="date_heure", y=production_fields, title="Production par filière", color_discrete_map=field_colors)
