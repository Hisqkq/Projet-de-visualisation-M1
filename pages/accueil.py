import dash
import dash_bootstrap_components as dbc
import threading
from dash import html, dcc, Output, Input, callback
from dash.exceptions import PreventUpdate

import view.figures as figures
import view.pie_chart as pie_chart
import view.story as story
from initialise_db import perform_update
from view.datepicker import default_start_date, default_end_date

dash.register_page(__name__, path='/')

update_thread = None
modal = dbc.Modal(
            dbc.ModalBody(
                html.Div(
                    [
                        html.P("Mise à jour des données en cours..."),
                        html.P("Cette opération peut prendre plusieurs minutes."),
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
    navbar = dbc.NavbarSimple(
        brand="Analyse de l'électricité en France Métropolitaine (Hors Corse)",
        color="primary",
        dark=True,
        className="mb-4",
        children=[
            dbc.Button("Mettre à jour les données", id="update-data-button", color="light", className="ms-auto")
        ],
        style={"fontSize": "1.5rem", "fontWeight": "bold"}  
    )

    card_style = {
        "margin": "1rem",  
        "boxShadow": "0px 0px 15px rgba(0,0,0,0.2)",  
    }

    card_header_style = {
        "fontSize": "1.5rem",  
        "fontWeight": "bold",  
        "color": "#FFFFFF",  
    }

    card_content_echanges = [
        dbc.CardHeader(
        [
            html.Img(src="/assets/echange.svg", style={"height": "2rem", "marginRight": "10px"}), 
            "Échanges"
        ],
        className="text-center",
        style=card_header_style
        ),
        dbc.CardBody(
            dcc.Link(
                dcc.Graph(
                    id='choropleth-map',
                    figure=figures.build_boxplot_echanges(default_start_date, default_end_date).update_layout(showlegend=False),
                    config={'displayModeBar': False}
                ),
                href=dash.page_registry['pages.echanges']['path']
            )
        )
    ]

    card_content_production = [
        dbc.CardHeader(
        [
            html.Img(src="/assets/production.svg", style={"height": "2rem", "marginRight": "10px"}), 
            "Production"
        ],
        className="text-center",
        style=card_header_style
        ),
        dbc.CardBody(
            dcc.Link(
                dcc.Graph(
                    id="pie_chart_production_par_filiere",
                    figure=pie_chart.metropolitan_pie_chart_production_by_field(is_title=False, background=True),
                    config={'displayModeBar': False}
                ),
                href=dash.page_registry['pages.production']['path']
            )
        )
    ]

    card_content_consommation = [
        dbc.CardHeader(
        [
            html.Img(src="/assets/consommation.svg", style={"height": "2rem", "marginRight": "10px"}),
            "Consommation"
        ],
        className="text-center",
        style=card_header_style
        ),
        dbc.CardBody(
            dcc.Link(
                dcc.Graph(
                    id="graph_consommation_prediction",
                    figure=figures.build_line_chart_with_prediction(default_start_date, default_end_date, homepage=True).update_layout(showlegend=False),
                    config={'displayModeBar': False}
                ),
                href=dash.page_registry['pages.consommation']['path']
            )
        )
    ]

    return dbc.Container([
        modal,
        navbar,
        dcc.Interval(id='interval-component', interval=500, n_intervals=0),
        dbc.Row([
            dbc.Col(dbc.Card(card_content_echanges, color="primary", outline=True, style=card_style), width=12, lg=4),
            dbc.Col(dbc.Card(card_content_production, color="primary", outline=True, style=card_style), width=12, lg=4),
            dbc.Col(dbc.Card(card_content_consommation, color="primary", outline=True, style=card_style), width=12, lg=4)
        ], className="mt-3 g-0"),
        dbc.Row([
            story.story_accueil()
        ]),
        html.Footer(html.P("PVA - Louis Delignac & Théo Lavandier & Hamad Tria - CMI ISI - 2023", className="text-center"))
    ], fluid=True)


@callback(
    Output("modal-spinner", "is_open"),
    [Input("update-data-button", "n_clicks"),
     Input("interval-component", "n_intervals")],
    prevent_initial_call=True
)
def handle_update_and_check_progress(n_clicks, n_intervals):
    """Handle the update of the data and check the progress of the update."""
    global update_thread

    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == "update-data-button":
        update_thread = threading.Thread(target=perform_update)
        update_thread.start()
        return True
    elif trigger_id == "interval-component":
        if update_thread and not update_thread.is_alive():
            return False
    raise PreventUpdate