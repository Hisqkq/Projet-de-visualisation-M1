from dash import register_page, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

import view.datepicker as datepicker
from view.datepicker import default_start_date, default_end_date
import view.figures as figures
import view.map as map

register_page(__name__)

def layout():
    return dbc.Container([
        dbc.NavbarSimple(
            brand="Les échanges commerciaux aux frontières", 
            color="primary", 
            dark=True, 
            className="mb-4"
        ),
        dbc.Row([
            dbc.Col(dcc.Link(html.Button('Accueil', className='btn btn-primary'), href='/'), width=12),
            dbc.Col(datepicker.datepicker, width=12),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(
                id='choropleth-map', 
                figure=map.build_metropolitan_map(),
                config={'displayModeBar': False}
            ), lg=6),
            dbc.Col(dcc.Graph(
                id="stacked_bar_chart_echanges", 
                figure=figures.build_stacked_bar_chart(["ech_comm_angleterre", "ech_comm_espagne", "ech_comm_italie", "ech_comm_suisse"], default_start_date, default_end_date)
            ), lg=6)
        ]),
        html.Footer(html.P("PVA - Louis Delignac & Théo Lavandier & Hamad Tria - CMI ISI - 2023", className="text-center"))
    ], fluid=True)


@callback(
    Output('stacked_bar_chart_echanges', 'figure'),
    Input("date-range-picker", "value"),
)
def update_bar_chart_echanges(dates):
    """Define dates to avoid callbak error."""
    if dates is None:
        dates = [default_start_date, default_start_date]
    return figures.build_stacked_bar_chart(
        arguments=[
            "ech_comm_angleterre", 
            "ech_comm_espagne", 
            "ech_comm_italie", 
            "ech_comm_suisse", 
            "ech_comm_allemagne_belgique"
        ], 
        starting_date=dates[0], 
        ending_date=dates[1]
    )