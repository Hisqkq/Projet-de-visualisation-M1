from dash import html, dcc
import plotly.express as px
import data.db_services as dbs


prodution_nucleaire = dbs.get_data_group_by_sum("eco2mix", "date", ["consommation", "ech_physiques", "eolien", "hydraulique", "nucleaire"], 1)

fig = px.line(prodution_nucleaire, x="_id", y="nucleaire")

données_1mars2023 = dbs.get_data_from_one_date("eco2mix", "2023-03-01")

fig2 = px.area(données_1mars2023, x="date_heure", y="nucleaire", color="libelle_region")

layout = html.Div(children=[
    html.Div(children='''
        Energie en France
    '''),
    html.H3(children="prodiction d'energie nucléaire"),
    dcc.Graph(figure=fig),
    dcc.Graph(figure=fig2)
    ])

