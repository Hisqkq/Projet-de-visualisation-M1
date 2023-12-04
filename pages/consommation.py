from dash import register_page, html, dcc, callback
from dash.dependencies import Input, Output
import view.figures as figures

register_page(__name__)

layout = html.Div([
    dcc.Link(html.Button('Home'), href='/'),
    dcc.Graph(
        id='choropleth-map',
        figure=figures.build_map(),
        config={'displayModeBar': False}
    ),
    dcc.Graph(figure=figures.line_chart_cons)
])
