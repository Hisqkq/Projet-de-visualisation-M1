import plotly.express as px
from dash import dcc

from view.map import *

def init_map():
    return dcc.Graph(id='choropleth-map')

def build_map():
    data = get_json()
    data = filter_metropolitan_regions(data)
    fig = build_metropolitan_map(data)
    return fig