from dash import html, dcc
import view.figures as figures

layout = html.Div(children=[
    html.Div(children='''
        Energie en France
    '''),
    html.H3(children="production d'energie nucléaire"),
    dcc.DatePickerRange(),
    dcc.Graph(figure=figures.fig),
    dcc.Graph(figure=figures.fig2)
    ])