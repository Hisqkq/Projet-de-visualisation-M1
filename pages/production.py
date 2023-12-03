from dash import register_page, html, dcc, callback
from dash.dependencies import Input, Output
import view.figures as figures
import view.GUI
from view import datepicker

register_page(__name__)

layout = html.Div([
    dcc.Link(html.Button('Home'), href='/'),
    datepicker.datepicker,
    dcc.Graph(
        id='choropleth-map',
        figure=view.GUI.build_map(),
        style={'height': '80vh'} 
    ),
 #   dcc.Graph(figure=figures.line_chart),
    dcc.Dropdown(["eolien", "hydraulique", "nucleaire", "solaire"], 'solaire', id="dropdown"),
    dcc.Graph(figure=figures.build_stacked_area_chart(figures.test_data_one_date, "solaire"), id="graph_production_stacked_area")
])



@callback(
    Output('choropleth-map', 'figure'),
    [Input('choropleth-map', 'clickData')]
)
def update_map(selected_data):
    if selected_data is None:
        return view.GUI.build_map()

    new_fig = view.map.build_region_map(view.map.filter_metropolitan_regions(view.map.get_json()), selected_data['points'][0]['location'])

    return new_fig

@callback(
    Output(component_id='graph_production_stacked_area', component_property='figure'),
    [Input(component_id='dropdown', component_property='value')]
)
def update_graph_production_stacked_area(value):
    return figures.build_stacked_area_chart(figures.test_data_one_date, value)