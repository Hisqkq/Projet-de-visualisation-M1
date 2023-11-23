from dash import html, dcc
import plotly.express as px
import data.db_services as dbs


df_consommation_quotidienne_brute = dbs.get_data_group_by_sum("eco2mix", "date", ["consommation", "ech_physiques", "eolien", "hydraulique", "nucleaire"], 1)

fig = px.line(df_consommation_quotidienne_brute, x="_id", y="nucleaire")

layout = html.Div(children=[
    html.Div(children='''
        Energie en France
    '''),
    html.H3(children="prodiction d'energie nucléaire"),
    dcc.Graph(figure=fig)
    ])