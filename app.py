import configparser
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, page_container

config = configparser.ConfigParser()
config.read('data/config.ini')

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div(
    style={'backgroundColor': str(config['Colors']['background'])},
    children=[
        dcc.Location(id="url"),
        page_container
    ]
)

if __name__ == '__main__':
    app.run(debug=True)