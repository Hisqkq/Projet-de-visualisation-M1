import plotly.express as px
import datetime

import data.db_services as dbs

def build_line_chart_with_prediction(date=datetime.datetime.now().strftime("%Y-%m-%d")):
    """Create a line chart.
    
    Parameters
    ----------
    date : str, optional
        Date, by default datetime.datetime.now().strftime("%Y-%m-%d").
        
    Returns
    -------
    plotly.graph_objects.Figure
        Figure containing the line chart.
    """
    # Fetching data and converting JSON to DataFrame
    json_data = dbs.get_data_from_one_date("DonneesNationales", date)
    data = dbs.transform_data_to_df(json_data)
    #Order data by datetime
    data = data.sort_values(by=['date_heure'])

    # Check if the necessary columns are in the DataFrame
    if not {'date_heure', 'consommation', 'prevision_j', 'prevision_j1'}.issubset(data.columns):
        raise ValueError("One or more required columns are missing in the data")

    # Creating the line chart
    line_chart_cons = px.area(data, x="date_heure", y="consommation")
    line_chart_cons.add_scatter(x=data["date_heure"], y=data["prevision_j"], mode='lines', name='Prediction J')
    line_chart_cons.add_scatter(x=data["date_heure"], y=data["prevision_j1"], mode='lines', name='Prediction J-1')

    return line_chart_cons


def build_pie_chart_production_by_field():
    """Create a pie chart.
    
    Returns
    -------
    plotly.graph_objects.Figure
        Figure containing the pie chart.
    """
    data = dbs.get_mean_by_date_from_one_date_to_another_date("DonneesNationales", "2020-01-01", "2020-01-02", ["eolien", "hydraulique", "nucleaire", "solaire", "fioul", "charbon", "gaz", "bioenergies"])[0]
    pie_chart_production_par_filiere = px.pie(names=list(data.keys()), values=list(data.values()), title='Répartition de la Production des Sources d’Énergie')
    pie_chart_production_par_filiere.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hoverinfo='label+percent',
        marker=dict(
            colors=px.colors.qualitative.Pastel1,
            line=dict(color='#FFFFFF', width=2)
        )
    )
    pie_chart_production_par_filiere.update_layout(
        showlegend=False,
        title=dict(
            font=dict(size=24)
        )
    )
    return pie_chart_production_par_filiere


def build_stacked_area_chart(argument = "nucleaire", date = datetime.datetime.now().strftime("%Y-%m-%d")):
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
    data = dbs.get_data_from_one_date("DonneesRegionales", date)
    return px.area(data, x="date_heure", y=str(argument), color="libelle_region", title=f"Production {argument}")


def build_stacked_bar_chart(arguments, starting_date, ending_date):
    """Create a stacked bar chart.
    
    Parameters
    ----------
    arguments : list
        List of arguments.
    starting_date : str
        Starting date.
    ending_date : str
        Ending date.
        
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
    fig = px.bar(data_melted, x='date_heure', y='value', color='category', barmode='stack')
    fig.update_layout(bargap=0.01)
    return fig