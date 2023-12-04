from dash import register_page, html, dcc
import dash_bootstrap_components as dbc

import view.figures as figures
import view.map as map

register_page(__name__, path='/')

layout = html.Div(
    children=[
        dbc.NavbarSimple(brand="L'électricité en France", color="primary", dark=True, className="mb-4"),
        dbc.Container([
            dbc.Row([
                dbc.Col(
                    dcc.Link(html.Div(
                        children=[
                            html.H1('Échanges'),
                            dcc.Graph(
                                id='choropleth-map',
                                figure=map.build_metropolitan_map(),
                                config={'displayModeBar': False}
                            ),
                        ]
                    ), href='/echanges'), width=4),
                dbc.Col(
                    dcc.Link(html.Div(
                        children=[
                            html.H1('Production'),
                            dcc.Graph(
                                id="pie_chart_production_par_filiere",
                                figure=figures.build_pie_chart_production_by_field().update_layout(title_text=""), # TODO: Fix title
                            )
                        ]
                    ), href='/production'), width=4),
                dbc.Col(
                    dcc.Link(html.Div(
                        children=[
                            html.H1('Consommation'),
                            dcc.Graph(
                                id="graph_consommation_prediction",
                                figure=figures.build_line_chart_with_prediction().update_layout(showlegend=False) # TODO: Fix legend
                            )
                        ]
                    ), href='/consommation'), width=4)
            ], className="mt-3")
        ]),
        html.Footer(html.P("PVA - Louis Delignac & Théo Lavandier & Hamad Tria - CMI ISI - 2023", className="text-center"))
    ]
)