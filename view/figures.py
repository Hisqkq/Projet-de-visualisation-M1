import plotly.express as px

import data.db_services as dbs
from view.datepicker import default_start_date, default_end_date

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
                                        end_date: str = default_end_date) -> px.pie:
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
    data = dbs.get_mean_by_date_from_one_date_to_another_date("DonneesNationales", start_date, end_date, ["eolien", "hydraulique", "nucleaire", "solaire", "fioul", "charbon", "gaz", "bioenergies"])[0]
    fig = px.pie(names=list(data.keys()), values=list(data.values()), title='Répartition de la Production des Sources d’Énergie')
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