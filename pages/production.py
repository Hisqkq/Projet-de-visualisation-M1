from dash import register_page, html, dcc, callback, no_update
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from view.datepicker import default_start_date, default_end_date
from view.datepicker import datepicker
import view.figures as figures
import view.map as map

register_page(__name__)

### Variables ###
france_map = map.build_metropolitan_map()
current_map_state = "France"
#################

def layout():
    return dbc.Container([
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
                    figure=figures.build_pie_chart_production_by_field())
            ], width=3),
            dbc.Col([
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
                    figure=figures.build_stacked_area_chart("solaire")),
            ], width=5)
        ]),
        html.Footer(html.P("PVA - Louis Delignac & Théo Lavandier & Hamad Tria - CMI ISI - 2023", className="text-center"))
    ], fluid=True)

@callback(
    Output('choropleth-map_production', 'figure'),
    [Input('choropleth-map_production', 'clickData')]
)
def update_map(selected_data):
    """Update the map when a region is selected."""
    global current_map_state # TODO: Fix this

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
    Output('graph_production_stacked_area', 'figure'),
    [Input('dropdown', 'value'),
     Input("date-range-picker", "value"),]
)
def update_graph_production_stacked_area(value, dates):
    """Update the stacked area chart."""
    if value is None or dates is None:
        return no_update
    return figures.build_stacked_area_chart(value.lower(), dates[0], dates[1])

@callback(
    Output('pie_chart_production_by_sector', 'figure'),
    [Input(component_id="date-range-picker", component_property="value"),]
)
def update_pie_chart_production_by_sector(dates):
    """Update the pie chart."""
    if dates is None:
        return no_update
    return figures.build_pie_chart_production_by_field(dates[0], dates[1])