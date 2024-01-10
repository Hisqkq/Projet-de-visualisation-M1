import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import urllib.parse
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
        dbc.Row([
            dmc.Select(
                placeholder="Choissez une région à comparer",
                id="select-region-to-compare1",
                data=[
                    {'value': 'Auvergne-Rhône-Alpes', 'label': 'Auvergne-Rhône-Alpes'},
                    {'value': 'Bourgogne-Franche-Comté', 'label': 'Bourgogne-Franche-Comté'},
                    {'value': 'Bretagne', 'label': 'Bretagne'},
                    {'value': 'Centre-Val de Loire', 'label': 'Centre-Val de Loire'},
                    {'value': 'Corse', 'label': 'Corse'},
                    {'value': 'Grand Est', 'label': 'Grand Est'},
                    {'value': 'Hauts-de-France', 'label': 'Hauts-de-France'},
                    {'value': 'Île-de-France', 'label': 'Île-de-France'},
                    {'value': 'Normandie', 'label': 'Normandie'},
                    {'value': 'Nouvelle-Aquitaine', 'label': 'Nouvelle-Aquitaine'},
                    {'value': 'Occitanie', 'label': 'Occitanie'},
                    {'value': 'Pays de la Loire', 'label': 'Pays de la Loire'},
                    {'value': 'Provence-Alpes-Côte d\'Azur', 'label': 'Provence-Alpes-Côte d\'Azur'},
                ], 
                value='Nouvelle-Aquitaine',
                style={"width": "25%"}
            ),
            dmc.Select(
                placeholder="Choissez une région à comparer",
                id="select-region-to-compare2",
                data=[
                    {'value': 'Auvergne-Rhône-Alpes', 'label': 'Auvergne-Rhône-Alpes'},
                    {'value': 'Bourgogne-Franche-Comté', 'label': 'Bourgogne-Franche-Comté'},
                    {'value': 'Bretagne', 'label': 'Bretagne'},
                    {'value': 'Centre-Val de Loire', 'label': 'Centre-Val de Loire'},
                    {'value': 'Corse', 'label': 'Corse'},
                    {'value': 'Grand Est', 'label': 'Grand Est'},
                    {'value': 'Hauts-de-France', 'label': 'Hauts-de-France'},
                    {'value': 'Île-de-France', 'label': 'Île-de-France'},
                    {'value': 'Normandie', 'label': 'Normandie'},
                    {'value': 'Nouvelle-Aquitaine', 'label': 'Nouvelle-Aquitaine'},
                    {'value': 'Occitanie', 'label': 'Occitanie'},
                    {'value': 'Pays de la Loire', 'label': 'Pays de la Loire'},
                    {'value': 'Provence-Alpes-Côte d\'Azur', 'label': 'Provence-Alpes-Côte d\'Azur'},
                ], 
                value='Occitanie',
                style={"width": "25%"}
            ),
            dcc.Link(
                id="comparer-button", 
                children=[
                    dbc.Button('Comparer', color="light", className="ms-auto"),
                ],
                href='/comparer/Nouvelle-Aquitaine-Alpes&Occitanie',
                style={"width": "25%"}
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
    Output('select-region-to-compare1', 'value'),
    [Input('memory-output', 'data')]
)
def update_select_region_to_compare1(data):
    """Update the first select region to compare."""
    if data == "France":
        return no_update
    return data

@callback(
    Output('comparer-button', 'href'),
    [Input('select-region-to-compare1', 'value'),
     Input('select-region-to-compare2', 'value')]
)
def update_comparer_button(region1, region2):
    """Update the comparer button."""
    return f'/comparer/{urllib.parse.quote(region1)}&{urllib.parse.quote(region2)}'

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