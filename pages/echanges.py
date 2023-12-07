from dash import register_page, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

import view.datepicker as datepicker
from view.datepicker import default_start_date, default_end_date
import view.figures as figures
import view.map as map

register_page(__name__)

layout = dbc.Container([
    dbc.NavbarSimple(brand="Les échanges commerciaux aux frontières", color="primary", dark=True, className="mb-4"),
    dbc.Row([
        dbc.Col(dcc.Link(html.Button('Home', className='btn btn-primary'), href='/'), width=12),
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
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_bar_chart_echanges(date1, date2):
    """Define dates to avoid callbak error."""
    if date1 is None and date2 is None:
        date1, date2 = default_start_date, default_start_date
    elif date1 is None:
        date1 = date2
    elif date2 is None:
        date2 = date1

    return figures.build_stacked_bar_chart(["ech_comm_angleterre", "ech_comm_espagne", "ech_comm_italie", "ech_comm_suisse"], date1, date2)