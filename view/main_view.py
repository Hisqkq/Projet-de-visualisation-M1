from dash import html, dcc
import view.figures as figures
import view.map as map

layout = html.Div(children=[
    html.Div(children='''
        Energie en France
    '''),
    html.H3(children="production d'energie nucléaire"),
    dcc.DatePickerRange(),
    dcc.Graph(figure=figures.line_chart),
    dcc.Graph(figure=figures.stacked_area_chart),
    dcc.Graph(figure=map.show_map(map.create_metropolitan_map(map.filter_metropolitan_regions(map.load_json(map.JSON))))),
    ])


