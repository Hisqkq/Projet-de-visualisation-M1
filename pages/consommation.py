from dash import register_page, html, dcc, callback
from dash.dependencies import Input, Output
import view.figures as figures

register_page(__name__)

layout = html.Div([
    dcc.Link(html.Button('Home'), href='/'),
    dcc.Graph(
        id='choropleth-map',
        figure=figures.build_map(),
        style={'height': '80vh'} 
    ),
    dcc.Graph(figure=figures.build_line_chart_with_prediction(), id="graph_consommation_prediction"),
])
