from dash import register_page, html, dcc, callback
from dash.dependencies import Input, Output
import view.figures as figures
import view.map as map

import view.map
import view.GUI

register_page(__name__)

layout = html.Div([
    dcc.Link(html.Button('Home'), href='/'),
    dcc.DatePickerRange(),
    dcc.Graph(
        id='choropleth-map',
        figure=view.GUI.build_map(),
        style={'height': '80vh'} 
    ),
    dcc.Graph(figure=figures.line_chart),
    dcc.Dropdown(["eolien", "hydraulique", "nucleaire", "solaire"], 'solaire', id="dropdown"),
    dcc.Graph(figure=figures.build_stacked_area_chart("solaire"), id="graph_production")
])



@callback(
    Output('choropleth-map', 'figure'),
    [Input('choropleth-map', 'clickData')]
)
def update_map(selected_data):
    if selected_data is None:
        return view.GUI.build_map()

    new_fig = view.map.build_region_map(view.map.filter_metropolitan_regions(view.map.get_json()), selected_data['points'][0]['location'])

    return new_fig