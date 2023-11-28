from dash import register_page, html, dcc, callback
from dash.dependencies import Input, Output

import view.map
import view.GUI

register_page(__name__)

layout = html.Div([
    dcc.Link(html.Button('Home'), href='/'),
    dcc.Graph(
        id='choropleth-map',
        figure=view.GUI.build_map(),
        style={'height': '80vh'} 
    )
])
