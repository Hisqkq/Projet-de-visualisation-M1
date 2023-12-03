import dash
from dash import html, dcc

import view.figures as figures

dash.register_page(__name__, path='/')

layout = html.Div(
    id='home',
    children=[
        dcc.Link(html.Div(
            children=[
                dcc.Graph(
                    id='choropleth-map',
                    figure=figures.build_map(),
                    config={'displayModeBar': False}
                ),
            ]
        ), href='/echanges'),
        dcc.Link(html.Div(
            children=[
                html.Img(src='./assets/images/production.png')
            ]
        ), href='/production'),
        dcc.Link(html.Div(
            children=[
                html.Img(src='./assets/images/consommation.png')
            ]
        ), href='/consommation')
    ]
)