from dash import Dash, html, dcc
from dash.dash_table import DataTable
import plotly.express as px
import pandas as pd
from data import api_service

app = Dash(__name__)

df_import_export = api_service.fetch_data_to_dataframe()
df_consommation_quotidienne_brute = api_service.fetch_data_consommation_quotidienne_brute()

table_import_export = DataTable(
    id='table_import_export',
    columns=[{"name": i, "id": i} for i in df_import_export.columns],
    data=df_import_export.to_dict('records'),
)

table_consommation_quotidienne_brute = DataTable(
    id='table_eco2mix',
    columns=[{"name": i, "id": i} for i in df_consommation_quotidienne_brute.columns],
    data=df_consommation_quotidienne_brute.to_dict('records'),
)

fig = px.bar(df_consommation_quotidienne_brute, x='region', y='somme_consommation_elec', color='region')

app.layout = html.Div(children=[
    html.H1(children='Tables des Données'),
    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
    html.H3(children='Table Import Export'),
    table_import_export,
    html.H3(children='Table consommation quotidienne brute par région'),
    table_consommation_quotidienne_brute,
    dcc.Graph(figure=fig)
])
if __name__ == '__main__':
    app.run(debug=True)