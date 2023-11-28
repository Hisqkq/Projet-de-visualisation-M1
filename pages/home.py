import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div(
    style={'background-color': '#475ba3'},
    children=[
        dcc.Link(html.Img(src='/assets/echanges.png'), href='/echanges'),
        dcc.Link(html.Img(src='/assets/production.png'), href='/production'),
        dcc.Link(html.Img(src='/assets/consommation.png'), href='/consommation')
    ]
)
