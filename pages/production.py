from dash import register_page, html, dcc, callback, no_update
from dash.dependencies import Input, Output
import view.figures as figures

register_page(__name__)

layout = html.Div([
    dcc.Link(html.Button('Home'), href='/'),
    dcc.DatePickerRange(),
    dcc.Graph(
        id='choropleth-map_production',
        figure=figures.build_map(),
        style={'height': '80vh'} 
    ),
    dcc.Graph(figure=figures.line_chart),
    dcc.Dropdown(["eolien", "hydraulique", "nucleaire", "solaire"], 'solaire', id="dropdown"),
    dcc.Graph(figure=figures.build_stacked_area_chart("solaire"), id="graph_production")
])


@callback(
    Output('choropleth-map_production', 'figure'),
    [Input('choropleth-map_production', 'clickData')]
)
def update_map(selected_data):
    if selected_data is None:
        return no_update

    new_fig = figures.build_map(selected_data['points'][0]['location'])

    return new_fig