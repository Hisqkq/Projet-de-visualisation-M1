import dash_bootstrap_components as dbc
from dash import register_page, html, dcc, callback, Output, Input, State, callback_context
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify

import view.datepicker as datepicker
import view.figures as figures
import view.map as map
import view.story as story
from view.datepicker import default_start_date, default_end_date

register_page(__name__)


def layout():
    return dbc.Container([
        dbc.NavbarSimple(brand="La consommation d'électricité en France",
                         color="primary",
                         dark=True,
                         className="mb-4",
                         children=[
                             dcc.Link(dbc.Button('Accueil',
                                                 color="light",
                                                 className="ms-auto"),
                                      href='/')
                         ],
                         style={
                             "fontSize": "1.5rem",
                             "fontWeight": "bold"
                         }),
        dbc.Col(datepicker.datepicker, width=12),
        dbc.Row([
            dbc.Col([
                dmc.Switch(id="switch-background-map",
                           offLabel=DashIconify(icon="tabler:background",
                                                width=20),
                           onLabel=DashIconify(icon="carbon:map", width=20),
                           size="lg",
                           style={"margin": "1rem"}),
                dcc.Graph(id='consommation-map',
                          figure=map.build_map_colors(default_start_date,
                                                      default_end_date),
                          config={'displayModeBar': False})
            ],
                    width=4),
            dbc.Col([
                dcc.Graph(
                    id="graph_consommation_prediction",
                    figure=figures.build_line_chart_with_prediction(
                        default_start_date, default_end_date),
                )
            ],
                    width=8),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id="graph_consommation_by_region",
                    figure=figures.build_line_chart_consommation_by_region(
                        default_start_date, default_end_date),
                    config={'displayModeBar': False})
            ],
                    width=12),
        ]),
        story.story_consommation(),
        html.Footer(
            html.
            P("PVA - Louis Delignac & Théo Lavandier & Hamad Tria - CMI ISI - 2023",
              className="text-center"))
    ],
                         fluid=True)


@callback(
    Output('graph_consommation_prediction', 'figure'),
    Input("date-range-picker", "value"),
)
def update_line_chart_with_prediction(dates):
    if dates is None:
        dates = [default_start_date, default_start_date]
    return figures.build_line_chart_with_prediction(starting_date=dates[0],
                                                    ending_date=dates[1])


@callback(
    Output('graph_consommation_by_region', 'figure'),
    Input("date-range-picker", "value"),
)
def update_line_chart_consommation_by_region(dates):
    if dates is None:
        dates = [default_start_date, default_start_date]
    return figures.build_line_chart_consommation_by_region(
        starting_date=dates[0], ending_date=dates[1])


@callback(Output('consommation-map', 'figure'), [
    Input("date-range-picker", "value"),
    Input("switch-background-map", "checked")
], [State('consommation-map', 'figure')])
def update_map(dates, checked, fig):
    ctx = callback_context

    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == "date-range-picker":
        if dates is None:
            dates = [default_start_date, default_start_date]
        fig = map.build_map_colors(dates[0], dates[1])
        if checked:
            fig['layout']['mapbox']['style'] = "carto-darkmatter"
        else:
            fig['layout']['mapbox'][
                'style'] = "mapbox://styles/tlavandier/clqmy8zxa00qt01o3ax462t6g"
    elif trigger_id == "switch-background-map":
        if checked:
            fig['layout']['mapbox']['style'] = "carto-darkmatter"
        else:
            fig['layout']['mapbox'][
                'style'] = "mapbox://styles/tlavandier/clqmy8zxa00qt01o3ax462t6g"

    return fig
