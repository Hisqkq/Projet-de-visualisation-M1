import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

import view.figures as figures

dash.register_page(__name__, path='/')

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
                                figure=figures.build_map(),
                                config={'displayModeBar': False}
                            ),
                        ]
                    ), href='/echanges'), width=4),
                dbc.Col(
                    dcc.Link(html.Div(
                        children=[
                            html.H1('Production'),
                            html.Img(src='./assets/images/production.png')
                        ]
                    ), href='/production'), width=4),
                dbc.Col(
                    dcc.Link(html.Div(
                        children=[
                            html.H1('Consommation'),
                            dcc.Graph(figure=figures.line_chart_cons)
                        ]
                    ), href='/consommation'), width=4)
            ], className="mt-3")
        ])
    ]
)