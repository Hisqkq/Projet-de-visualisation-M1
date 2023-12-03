import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div(
    id='home',
    children=[
        dcc.Link(html.Div(
            children=[
                html.Img(src='./assets/images/echanges.png')
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