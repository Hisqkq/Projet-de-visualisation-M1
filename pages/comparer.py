import dash
import dash_bootstrap_components as dbc
import urllib.parse
from dash import dcc, html, register_page

import view.pie_chart as pie_chart

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
            dbc.Col([
                dcc.Graph(
                    id="production_pie_chart_by_sector",
                    figure=pie_chart.region_pie_chart_production_by_field(region1),
                    config={'displayModeBar': False}
                )
            ], width=6),
            dbc.Col([
                dcc.Graph(
                    id="production_pie_chart_by_sector",
                    figure=pie_chart.region_pie_chart_production_by_field(region2),
                    config={'displayModeBar': False}
                )
            ], width=6)
        ]),
        html.Footer(html.P("PVA - Louis Delignac & Théo Lavandier & Hamad Tria - CMI ISI - 2023", className="text-center"))
    ], fluid=True)