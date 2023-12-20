from dash import register_page, html, dcc, callback, no_update
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from view.datepicker import datepicker
import view.figures as figures
import view.map as map
import view.pie_chart as pie_chart

register_page(__name__)

### Variables ###
france_map = map.build_metropolitan_map()
#################

def layout():
    return dbc.Container([
        dcc.Store(
            id='memory-output',
            data="France"
        ),
        dbc.NavbarSimple(
            brand="La production d'électricité en France", 
            color="primary", 
            dark=True, 
            className="mb-4"
        ),
        dbc.Col(dcc.Link(html.Button('Accueil', className='btn btn-primary'), href='/'), width=12),
        datepicker,
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id='choropleth-map_production',
                    figure=france_map,
                    config={'displayModeBar': False}
                )
            ], width=4),
            dbc.Col([
                dcc.Graph(
                    id="pie_chart_production_by_sector",
                    figure=pie_chart.build_metropolitan_pie_chart_production_by_field(),
                    config={'displayModeBar': False}
                ),
                dcc.Dropdown(
                    id="dropdown",
                    options=[
                        {'label': 'Eolien', 'value': 'eolien'},
                        {'label': 'Hydraulique', 'value': 'hydraulique'},
                        {'label': 'Nucléaire', 'value': 'nucleaire'},
                        {'label': 'Solaire', 'value': 'solaire'}
                    ],
                    value='solaire'
                ),
                dcc.Graph(
                    id="graph_production_stacked_area",
                    figure=figures.build_stacked_area_chart(argument="solaire"),
                    config={'displayModeBar': False}
                ),
                dcc.Graph(
                    id="graph_area_by_production_field", 
                    figure=figures.build_stacked_area_by_production(),
                    config={'displayModeBar': False}
                )
            ], width=8)
        ]),
        html.Footer(html.P("PVA - Louis Delignac & Théo Lavandier & Hamad Tria - CMI ISI - 2023", className="text-center"))
    ], fluid=True)

@callback(
    Output('choropleth-map_production', 'figure'),
    Output('memory-output', 'data'),
    [Input('choropleth-map_production', 'clickData'),
     State('memory-output', 'data')]
)
def update_map(selected_data, data):
    """Update the map when a region is selected."""
    if selected_data is None:
        return no_update

    if data == "France":
        return map.build_region_map(selected_data['points'][0]['location']), selected_data['points'][0]['location']
    return france_map, "France"

@callback(
    Output('pie_chart_production_by_sector', 'figure'),
    [Input('date-range-picker', 'value'),
     Input('memory-output', 'data'),]
)
def update_pie_chart_production_by_sector(dates, current_map_state):
    """Update the pie chart."""
    if dates is None:
        return no_update

    if current_map_state == "France":
        return pie_chart.build_metropolitan_pie_chart_production_by_field(dates[0], dates[1])
    return pie_chart.build_region_pie_chart_production_by_field(current_map_state, dates[0], dates[1])

@callback(
    Output('graph_production_stacked_area', 'figure'),
    [Input('dropdown', 'value'),
     Input('date-range-picker', 'value'),]
)
def update_graph_production_stacked_area(value, dates): # TODO: sync avec la map
    """Update the stacked area chart."""
    if value is None or dates is None:
        return no_update
    return figures.build_stacked_area_chart(value.lower(), dates[0], dates[1])