import dash
import dash_bootstrap_components as dbc
import urllib.parse
from dash import dcc, html, register_page, callback, Output, Input
import re

import view.pie_chart as pie_chart
import view.figures as figures
import view.datepicker as datepicker

register_page(__name__, path_template="/comparer/<region1>&<region2>")

def layout(region1, region2):
    region1 = urllib.parse.unquote(region1)
    region2 = urllib.parse.unquote(region2)
    if not (region1, region2 in 
            ["Auvergne-Rhône-Alpes", "Bourgogne-Franche-Comté", "Bretagne", 
             "Centre-Val de Loire", "Corse", "Grand Est", "Hauts-de-France", 
             "Île-de-France", "Normandie", "Nouvelle-Aquitaine", "Occitanie", 
             "Pays de la Loire", "Provence-Alpes-Côte d'Azur"]):
        return html.Div("Erreur : une ou plusieurs des régions n'existe pas")
    return dbc.Container([
        dbc.NavbarSimple(
            brand=f"La production d'électricité en {region1} et {region2}", 
            color="primary", 
            dark=True, 
            className="mb-4",
            children=[
                dcc.Link(dbc.Button('Retour', color="light", className="ms-auto"), href=dash.page_registry['pages.production']['path']),
                dcc.Link(dbc.Button('Accueil', color="light", className="ms-auto"), href='/')
            ],
            style={"fontSize": "1.5rem", "fontWeight": "bold"}  
        ),
        dbc.Row([
            dbc.Col(datepicker.datepicker, width=12),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id="production_pie_chart_by_sector_1",
                    figure=pie_chart.regional_pie_chart_production_by_sector(region1),
                    config={'displayModeBar': False}
                )
            ], width=6),
            dbc.Col([
                dcc.Graph(
                    id="production_pie_chart_by_sector_2",
                    figure=pie_chart.regional_pie_chart_production_by_sector(region2),
                    config={'displayModeBar': False}
                )
            ], width=6)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id="stacked_area_chart_by_region",
                    figure=figures.build_stacked_area_two_regions(region1, region2),
                    config={'displayModeBar': False}
                )
            ]),
        ]),
        html.Footer(html.P("PVA - Louis Delignac & Théo Lavandier & Hamad Tria - CMI ISI - 2023", className="text-center"))
    ], fluid=True)

@callback(
    [Output("production_pie_chart_by_sector_1", "figure"),
     Output("production_pie_chart_by_sector_2", "figure"),
     Output("stacked_area_chart_by_region", "figure")],
    [Input('url', 'pathname'),
     Input('date-range-picker', 'value')]
)
def update_graphs(pathname, dates):
    match = re.search(r'/comparer/(.+)&(.+)', pathname)
    if match:
        region1, region2 = match.groups()
        region1 = urllib.parse.unquote(region1)
        region2 = urllib.parse.unquote(region2)
        starting_date, ending_date = dates or [None, None]

        pie_chart_1 = pie_chart.regional_pie_chart_production_by_sector(region1, starting_date, ending_date)
        pie_chart_2 = pie_chart.regional_pie_chart_production_by_sector(region2, starting_date, ending_date)
        stacked_area_chart = figures.build_stacked_area_two_regions(region1, region2, starting_date, ending_date)

        return pie_chart_1, pie_chart_2, stacked_area_chart

    return dash.no_update, dash.no_update, dash.no_update
