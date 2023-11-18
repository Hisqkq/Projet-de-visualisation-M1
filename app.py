from dash import Dash, html, dcc
from dash.dash_table import DataTable
import plotly.express as px
import data.db_services as dbs

app = Dash(__name__)

df_consommation_quotidienne_brute = dbs.get_data_group_by_sum("eco2mix", "date", ["consommation", "ech_physiques", "eolien", "hydraulique", "nucleaire"], 1)

fig = px.line(df_consommation_quotidienne_brute, x="_id", y="nucleaire")


app.layout = html.Div(children=[
    html.Div(children='''
        Energie en France
    '''),
    html.H3(children="prodiction d'energie nucléaire"),
    dcc.Graph(figure=fig)
    ])
if __name__ == '__main__':
    app.run(debug=True)