from dash import register_page, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

from view.datepicker import default_start_date, default_end_date
import view.datepicker as datepicker
import view.figures as figures
import view.map as map

register_page(__name__)

def layout():
    return dbc.Container([
        dbc.NavbarSimple(
            brand="La consommation d'électricité en France", 
            color="primary", 
            dark=True, 
            className="mb-4"
        ),
        dbc.Col(dcc.Link(html.Button('Accueil', className='btn btn-primary'), href='/'), width=12),
        dbc.Col(datepicker.datepicker, width=12),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id='choropleth-map',
                    figure=map.build_metropolitan_map(),
                    config={'displayModeBar': False}
                )
            ], width=4),
            dbc.Col([
                dcc.Graph(
                    id="graph_consommation_prediction",
                    figure=figures.build_line_chart_with_prediction(default_start_date, default_end_date),
                )
            ], width=8),
        ]),
        html.Footer(html.P("PVA - Louis Delignac & Théo Lavandier & Hamad Tria - CMI ISI - 2023", className="text-center"))
    ], fluid=True)

@callback(
    Output('graph_consommation_prediction', 'figure'),
    Input("date-range-picker", "value"),
)
def update_line_chart_with_prediction(dates):
    """Define dates to avoid callbak error."""
    if dates is None:
        dates = [default_start_date, default_start_date]
    return figures.build_line_chart_with_prediction( 
        starting_date=dates[0], 
        ending_date=dates[1]
    )