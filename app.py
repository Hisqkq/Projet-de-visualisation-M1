from dash import Dash, html, dcc
from dash.dash_table import DataTable
import plotly.express as px
from data import api_service #should be deleted later, api shouldnt be accessed by view
from data.db_manager import data_to_df #should be deleted later, data should only be taken from datasets.py

import data.datasets as datasets


app = Dash(__name__)

df_import_export = api_service.fetch_data_to_dataframe("eco2mix-regional-tr")
df_consommation_quotidienne_brute = data_to_df("sum_cons_par_regions")

df_production = datasets.df_production

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
fig2 = px.line(df_production, x="_id", y="nucleaire", labels={"_id": "Date"})


app.layout = html.Div(children=[
    html.H1(children='Tables des Données'),
    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
    html.H3(children='Table Eco2mix'),
    dcc.Graph(figure=fig2),
    table_import_export,
    html.H3(children='Table consommation quotidienne brute par région'),
    table_consommation_quotidienne_brute,
    dcc.Graph(figure=fig)
    ])
if __name__ == '__main__':
    app.run(debug=True)