from dash import register_page, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import data.db_services as db_services
import view.datepicker as datepicker

import view.figures as figures

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
            figure=figures.build_map(),
            config={'displayModeBar': False}
        ), lg=6),
        dbc.Col(dcc.Graph(id="stacked_bar_chart_echanges", 
                          figure=figures.build_stacked_bar_chart(
                              db_services.get_data_from_one_date_to_another_date('DonneesNationales', "2020-06-08", "2020-06-09"), 
                              ["ech_comm_angleterre", "ech_comm_espagne", "ech_comm_italie", "ech_comm_suisse"])), lg=6)
    ]),
    html.Footer(html.P("PVA - CMI ISI - 2023", className="text-center"))
], fluid=True)


@callback(
    Output('stacked_bar_chart_echanges', 'figure'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_bar_chart_echanges(date1, date2):
    if date1 is None and date2 is None: # Avoid error with callback
        return figures.build_stacked_bar_chart(db_services.get_data_from_one_date_to_another_date('DonneesNationales', "2020-06-08", "2020-06-09"), ["ech_comm_angleterre", "ech_comm_espagne", "ech_comm_italie", "ech_comm_suisse"])
    if date2 is None:
        return figures.build_stacked_bar_chart(db_services.get_data_from_one_date_to_another_date('DonneesNationales', date1, date1), ["ech_comm_angleterre", "ech_comm_espagne", "ech_comm_italie", "ech_comm_suisse"])
    return figures.build_stacked_bar_chart(db_services.get_data_from_one_date_to_another_date('DonneesNationales', date1, date2), ["ech_comm_angleterre", "ech_comm_espagne", "ech_comm_italie", "ech_comm_suisse"])
