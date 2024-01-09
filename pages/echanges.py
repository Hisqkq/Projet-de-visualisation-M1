import dash_bootstrap_components as dbc
from dash import register_page, html, dcc, callback, Output, Input

import view.datepicker as datepicker
import view.figures as figures
from view.datepicker import default_start_date, default_end_date

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
                id='donut_chart_echanges',
                figure=figures.build_donuts_exchanges(default_start_date, default_end_date),
                config={'displayModeBar': False}
            ), lg=6),
            dbc.Col(dcc.Graph(
                id="stacked_bar_chart_echanges", 
                figure=figures.build_stacked_bar_chart(["ech_comm_angleterre", "ech_comm_espagne", "ech_comm_italie", "ech_comm_suisse", "ech_comm_allemagne_belgique"], default_start_date, default_end_date),
                config={'displayModeBar': False}
            ), lg=6)
        ]),
        dbc.Row([
            dcc.Graph(id="boxplot_echanges", figure=figures.build_boxplot_echanges(default_start_date, default_end_date), config={'displayModeBar': False})
        ]),
        html.Footer(html.P("PVA - Louis Delignac & Théo Lavandier & Hamad Tria - CMI ISI - 2023", className="text-center"))
    ], fluid=True)


@callback(
    Output('stacked_bar_chart_echanges', 'figure'),
    Input("date-range-picker", "value"),
)
def update_bar_chart_echanges(dates):
    """Update the stacked bar chart of the page."""
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


@callback(
    Output('boxplot_echanges', 'figure'),
    Input("date-range-picker", "value"),
)
def update_boxplot_echanges(dates):
    """Update the boxplot of the page."""
    if dates is None:
        dates = [default_start_date, default_start_date]
    return figures.build_boxplot_echanges(starting_date=dates[0], ending_date=dates[1])

@callback(
    Output('donut_chart_echanges', 'figure'),
    Input("date-range-picker", "value"),
)
def update_donut_chart_echanges(dates):
    """Update the donut chart of the page."""
    if dates is None:
        dates = [default_start_date, default_start_date]
    return figures.build_donuts_exchanges(starting_date=dates[0], ending_date=dates[1])