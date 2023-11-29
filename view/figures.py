import plotly.express as px
import data.db_services as dbs
from dash import Dash, html, dcc, Input, Output, callback


#### data used by graphs ####

prodution = dbs.get_data_group_by_sum("DonneesRegionales", "date", ["consommation", "ech_physiques", "eolien", "hydraulique", "nucleaire", "solaire"], 1)
données_1mars2023 = dbs.get_data_from_one_date("DonneesRegionales", "2022-09-12")
données_echanges = dbs.get_data_from_one_date("DonneesNationales", "2013-08-18")


#### graphs ####

line_chart = px.line(prodution, x="_id", y="solaire", labels={
                     "_id": "Date",
                     "solaire": "Production solaire",
                 },
                title="Production d'enérgie solaire en France")

line_chart_cons = px.bar(données_echanges, x="date_heure", y="consommation")

def build_stacked_area_chart(argument):
    return px.area(données_1mars2023, x="date_heure", y=str(argument), color="libelle_region", title=f"Production {argument}")

stacked_area_chart_echanges = px.bar(données_echanges, x="date_heure", y=["ech_comm_angleterre", "ech_comm_espagne", "ech_comm_italie", "ech_comm_suisse"])



@callback(
    Output(component_id='graph_production', component_property='figure'),
    Input(component_id='dropdown', component_property='value')
)
def update_graph(value):
    return build_stacked_area_chart(value)