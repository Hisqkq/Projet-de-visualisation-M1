import plotly.express as px
import data.db_services as dbs
import pandas as pd
import datetime

import view.map


def build_map(scope: str = 'France') -> px.choropleth:
    data = view.map.get_json()
    data = view.map.exclude_overseas_and_corsica(data)
    if scope != 'France':
        fig = view.map.build_region_map(data, scope)
    else:
        fig = view.map.build_metropolitan_map(data)
    return fig


def build_line_chart_with_prediction(date=datetime.datetime.now().strftime("%Y-%m-%d")):
    # Fetching data and converting JSON to DataFrame
    json_data = dbs.get_data_from_one_date("DonneesNationales", date)
    data = pd.DataFrame(json_data)

    # Check if the necessary columns are in the DataFrame
    if not {'date_heure', 'consommation', 'prevision_j', 'prevision_j1'}.issubset(data.columns):
        raise ValueError("One or more required columns are missing in the data")

    # Creating the line chart
    line_chart_cons = px.area(data, x="date_heure", y="consommation")
    line_chart_cons.add_scatter(x=data["date_heure"], y=data["prevision_j"], mode='lines', name='Prediction J')
    line_chart_cons.add_scatter(x=data["date_heure"], y=data["prevision_j1"], mode='lines', name='Prediction J-1')

    return line_chart_cons


def build_pie_chart_production_par_filiere():
    """Create a pie chart.
    
    Args:
        data (dict): Dictionary containing the data.
    Returns:
        plotly.graph_objects.Figure: Figure containing the pie chart."""
        
    data = dbs.get_average_values("DonneesNationales", ["eolien", "hydraulique", "nucleaire", "solaire", "fioul", "charbon", "gaz", "bioenergies"])

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
        showlegend=True,
        legend=dict(
            title='Sources d’Énergie',
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        ),
        title=dict(
            font=dict(size=24)
        )
    )
    return pie_chart_production_par_filiere


def build_stacked_area_chart(argument = "nucleaire", date = datetime.datetime.now().strftime("%Y-%m-%d")):
    data = dbs.get_data_from_one_date("DonneesRegionales", date)
    return px.area(data, x="date_heure", y=str(argument), color="libelle_region", title=f"Production {argument}")


def build_stacked_bar_chart(arguments, starting_date, ending_date):
    # Fetching data and converting JSON to DataFrame
    json_data = dbs.get_data_from_one_date_to_another_date("DonneesNationales", starting_date, ending_date)
    data = pd.DataFrame(json_data)
    
    # Convert all the string values to float
    for arg in arguments:
        data[arg] = data[arg].astype(float)

    # Check if the necessary columns are in the DataFrame
    if not all(arg in data.columns for arg in arguments):
        raise ValueError("One or more specified arguments are not in the data")

    # Reshaping the data for stacked bar chart
    data_melted = data.melt(id_vars='date_heure', value_vars=arguments, var_name='category', value_name='value')

    # Creating the stacked bar chart
    return px.bar(data_melted, x='date_heure', y='value', color='category', barmode='stack')