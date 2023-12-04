from dash import register_page, html, dcc, callback, no_update
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import view.figures as figures
import view.map as map
from view.datepicker import datepicker

register_page(__name__)

### Variables ###
france_map = map.build_metropolitan_map()
current_map_state = "France"
#################

layout = html.Div([
    dbc.NavbarSimple(brand="La production d'électricité en France", color="primary", dark=True, className="mb-4"),
    dcc.Link(html.Button('Home'), href='/'),
    datepicker,
    dcc.Graph(
        id='choropleth-map_production',
        figure=france_map,
        config={'displayModeBar': False}
    ),
 #   dcc.Graph(figure=figures.line_chart),
    dcc.Dropdown(["eolien", "hydraulique", "nucleaire", "solaire"], 'solaire', id="dropdown"),
    dcc.Graph(figure=figures.build_stacked_area_chart(figures.test_data_one_date, "solaire"), id="graph_production_stacked_area"),
    dcc.Graph(figure=figures.build_pie_chart_production_par_filiere(figures.production_par_filiere), id="pie_chart_production_par_filiere"),
    html.Footer(html.P("PVA - Louis Delignac & Théo Lavandier & Hamad Tria - CMI ISI - 2023", className="text-center"))
])


@callback(
    Output('choropleth-map_production', 'figure'),
    [Input('choropleth-map_production', 'clickData')]
)
def update_map(selected_data):
    """Update the map when a region is selected."""
    global current_map_state

    if selected_data is None:
        return no_update

    if current_map_state == "France":
        new_fig = map.build_region_map(selected_data['points'][0]['location'])
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