from dash import register_page, html, dcc, callback, no_update
from dash.dependencies import Input, Output
import time

import view.figures as figures
from view.datepicker import datepicker

register_page(__name__)

### Variables ###
france_map = figures.build_map()
current_map_state = "France"
#################

layout = html.Div([
    dcc.Link(html.Button('Home'), href='/'),
    datepicker,
    dcc.Graph(
        id='choropleth-map_production',
        figure=france_map,
        config={'displayModeBar': False}
    ),
 #   dcc.Graph(figure=figures.line_chart),
    dcc.Dropdown(["eolien", "hydraulique", "nucleaire", "solaire"], 'solaire', id="dropdown"),
    dcc.Graph(figure=figures.build_stacked_area_chart(figures.test_data_one_date, "solaire"), id="graph_production_stacked_area")
])


@callback(
    Output('choropleth-map_production', 'figure'),
    [Input('choropleth-map_production', 'clickData')]
)
def update_map(selected_data):
    global current_map_state

    if selected_data is None:
        return no_update

    if current_map_state == "France":
        new_fig = figures.build_map(selected_data['points'][0]['location'])
        current_map_state = "Region"
    else:
        new_fig = france_map
        current_map_state = "France"

    return new_fig

@callback(
    Output(component_id='graph_production_stacked_area', component_property='figure'),
    [Input(component_id='dropdown', component_property='value')]
)
def update_graph_production_stacked_area(value):
    return figures.build_stacked_area_chart(figures.test_data_one_date, value)