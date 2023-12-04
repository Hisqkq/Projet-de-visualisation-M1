import plotly.express as px
import data.db_services as dbs

#### data used by graphs ####

prodution = dbs.get_data_group_by_sum("DonneesRegionales", "date_heure", ["consommation", "ech_physiques", "eolien", "hydraulique", "nucleaire", "solaire"], 1)
test_data_one_date = dbs.get_data_from_one_date("DonneesRegionales", "2013-01-12")
données_echanges = dbs.get_data_from_one_date("DonneesNationales", "2020-07-02")
production_par_filiere = dbs.get_average_values("DonneesNationales", ["eolien", "hydraulique", "nucleaire", "solaire", "fioul", "charbon", "gaz", "bioenergies"])

#### graphs ####
line_chart = px.line(prodution, x="_id", y="solaire", labels={
                     "_id": "date_heure",
                     "solaire": "Production solaire",
                 },
                title="Production d'enérgie solaire en France")

line_chart_cons = px.bar(données_echanges, x="date_heure", y="consommation")


def build_stacked_area_chart(data, argument):
    return px.area(data, x="date_heure", y=str(argument), color="libelle_region", title=f"Production {argument}")


def build_stacked_bar_chart(data, arguments):
    return px.bar(data, x="date_heure", y=arguments)

stacked_area_chart_echanges = px.bar(données_echanges, x="date_heure", y=["ech_comm_angleterre", "ech_comm_espagne", "ech_comm_italie", "ech_comm_suisse"])


def build_pie_chart_production_par_filiere(data):
    """Create a pie chart.
    
    Args:
        data (dict): Dictionary containing the data.
    Returns:
        plotly.graph_objects.Figure: Figure containing the pie chart."""
    pie_chart_production_par_filiere = px.pie(names=list(data.keys()), values=list(data.values()), title='Répartition de la Production des Sources d’Énergie')
    # Customize the pie chart layout
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
