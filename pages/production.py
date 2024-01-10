import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import register_page, html, dcc, callback, no_update
from dash.dependencies import Input, Output, State

import view.figures as figures
import view.map as map
import view.pie_chart as pie_chart
from view.datepicker import datepicker

register_page(__name__)

### Data ###
france_map = map.build_metropolitan_map()
############

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
            className="mb-4",
            children=[
                dcc.Link(dbc.Button('Accueil', color="light", className="ms-auto"), href='/')
            ],
            style={"fontSize": "1.5rem", "fontWeight": "bold"}  
        ),
        datepicker,
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id='choropleth_map_production',
                    figure=france_map,
                    config={'displayModeBar': False}
                )
            ], width=4),
            dbc.Col([
                dcc.Graph(
                    id="production_pie_chart_by_sector",
                    figure=pie_chart.metropolitan_pie_chart_production_by_field(),
                    config={'displayModeBar': False}
                )
            ], width=8)
        ]),
        dbc.Row([
            html.Div(
                [
                    html.H4("Production régionale par type d'énergie", className="text-center mb-3"),
                    dmc.Select(
                        placeholder="Choose a production field",
                        id="select-energy-type",
                        data=[
                            {'value': 'eolien', 'label': 'Éolien'},
                            {'value': 'hydraulique', 'label': 'Hydraulique'},
                            {'value': 'nucleaire', 'label': 'Nucléaire'},
                            {'value': 'solaire', 'label': 'Solaire'},
                            {'value': 'thermique', 'label': 'Thermique'},
                        ],
                        value='solaire',  
                        style={"width": "33%", "cebter": "true"}
                    ),],
                ),
                dcc.Graph(
                id="graph_production_stacked_area",
                figure=figures.build_stacked_area_chart(argument="solaire"),
                config={'displayModeBar': False}
            )
        ]),
            
        html.Footer(html.P("PVA - Louis Delignac & Théo Lavandier & Hamad Tria - CMI ISI - 2023", className="text-center"))
    ], fluid=True)

@callback(
    Output('choropleth_map_production', 'figure'),
    Output('memory-output', 'data'),
    [Input('choropleth_map_production', 'clickData'),
     State('memory-output', 'data')]
)
def update_map(selected_data, data):
    """Update the map when a region is selected."""
    if selected_data is None:
        return no_update
    
    if data == "France":
        fig = map.build_region_map(selected_data['points'][0]['location'])
        return fig, selected_data['points'][0]['location']
    return france_map, "France"

@callback(
    Output('production_pie_chart_by_sector', 'figure'),
    [Input('date-range-picker', 'value'),
     Input('memory-output', 'data'),]
)
def update_production_pie_chart_by_sector(dates, current_map_state):
    """Update the pie chart."""
    if dates is None:
        return no_update

    if current_map_state == "France":
        return pie_chart.metropolitan_pie_chart_production_by_field(dates[0], dates[1])
    return pie_chart.region_pie_chart_production_by_field(current_map_state, dates[0], dates[1])

@callback(
    Output('graph_production_stacked_area', 'figure'),
    [Input('select-energy-type', 'value'),
     Input('date-range-picker', 'value'),]
)
def update_graph_production_stacked_area(value, dates): # TODO: sync avec la map
    """Update the stacked area chart."""
    if value is None or dates is None:
        return no_update
    return figures.build_stacked_area_chart(value.lower(), dates[0], dates[1])