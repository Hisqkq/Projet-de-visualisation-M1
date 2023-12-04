from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div(
    children=[
        dcc.Location(id="url"),
        page_container
    ]
)

if __name__ == '__main__':
    app.run(debug=True)