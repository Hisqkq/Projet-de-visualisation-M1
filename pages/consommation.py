from dash import register_page, html, dcc
import dash_bootstrap_components as dbc

import view.figures as figures
import view.map as map

register_page(__name__)

layout = html.Div([
    dbc.NavbarSimple(brand="La consommation d'électricité en France", color="primary", dark=True, className="mb-4"),
    dcc.Link(html.Button('Home'), href='/'),
    dcc.Graph(
        id='choropleth-map',
        figure=map.build_metropolitan_map(),
        config={'displayModeBar': False}
    ),
    dcc.Graph(figure=figures.build_line_chart_with_prediction(), id="graph_consommation_prediction"),
    html.Footer(html.P("PVA - Louis Delignac & Théo Lavandier & Hamad Tria - CMI ISI - 2023", className="text-center"))
])
