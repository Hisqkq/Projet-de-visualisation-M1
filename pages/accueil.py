import dash
from dash import html, dcc, Output, Input, callback
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import threading

from view.datepicker import default_start_date, default_end_date
import view.figures as figures
import view.map as map
import view.pie_chart as pie_chart
from data.db_constructor import update_data

dash.register_page(__name__, path='/')

modal = dbc.Modal(
            dbc.ModalBody(
                html.Div(
                    [
                        html.P("Mise à jour des données en cours..."),
                        html.P("Cette opéraiton peut prendre plusieurs minutes."),
                        dbc.Spinner(size="lg", color="primary"),
                    ]
                ),
                className="d-flex justify-content-center"
            ),
            id="modal-spinner",
            is_open=False,
            backdrop="static",
            keyboard=False, 
        )

def layout():
    return dbc.Container([
        modal,
        dcc.Interval(id='interval-component', interval=500, n_intervals=0),
        dbc.NavbarSimple(brand="L'électricité en France", color="primary", dark=True, className="mb-4"),
        dbc.Container([
            dbc.Row([
                dbc.Col(
                    dcc.Link(html.Div(
                        children=[
                            html.H1('Échanges'),
                            dcc.Graph(
                                id='choropleth-map',
                                figure=map.build_metropolitan_map(background=True),
                                config={'displayModeBar': False}
                            ),
                        ]
                    ), href=dash.page_registry['pages.echanges']['path']), width=4),
                dbc.Col(
                    dcc.Link(html.Div(
                        children=[
                            html.H1('Production'),
                            dcc.Graph(
                                id="pie_chart_production_par_filiere",
                                figure=pie_chart.build_metropolitan_pie_chart_production_by_field(is_title=False, background=True),
                                config={'displayModeBar': False}
                            )
                        ]
                    ), href=dash.page_registry['pages.production']['path']), width=4),
                dbc.Col(    
                    dcc.Link(html.Div(
                        children=[
                            html.H1('Consommation'),
                            dcc.Graph(
                                id="graph_consommation_prediction",
                                figure=figures.build_line_chart_with_prediction(default_start_date, default_end_date, homepage=True).update_layout(showlegend=False),
                                config={'displayModeBar': False}
                            )
                        ]
                    ), href=dash.page_registry['pages.consommation']['path']), width=4)
            ], className="mt-3"),
            dbc.Row([
                dbc.Button(
                    "Mettre à jours les données", id="update-data-button", color="primary", className="mb-3"
                )
            ]),
        ]),
        html.Footer(html.P("PVA - Louis Delignac & Théo Lavandier & Hamad Tria - CMI ISI - 2023", className="text-center"))
    ], fluid=True)
        
def perform_update():   # TODO: Put this function in data, and use it from there (not working for now)
    """Update data from RTE's API
    """
    update_data("eco2mix-national-tr", "DonneesNationales")
    update_data("eco2mix-regional-tr", "DonneesRegionales")

update_thread = None

@callback(
    Output("modal-spinner", "is_open"),
    [Input("update-data-button", "n_clicks"),
     Input("interval-component", "n_intervals")],
    prevent_initial_call=True
)
def handle_update_and_check_progress(n_clicks, n_intervals):
    global update_thread

    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == "update-data-button":
        update_thread = threading.Thread(target=perform_update) # Not working when perform_update is imported from data.db_constructor
        update_thread.start()
        return True
    elif trigger_id == "interval-component":
        if update_thread and not update_thread.is_alive():
            return False
    raise PreventUpdate