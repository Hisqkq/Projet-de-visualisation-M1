import dash
from dash import dcc, html, callback
from dash.dependencies import Input, Output

datepicker = html.Div([
    html.H1('Date Picker'),

    html.Label('Select Date(s):'),
    dcc.DatePickerRange(
        id='date-picker',
        start_date=None,
        end_date_placeholder_text='Select end date',
        calendar_orientation='vertical'
    ),

    html.Button('Clear', id='clear-button', n_clicks=0, style={'margin-top': '10px'}),

    html.Div(id='output')
])

@callback(
    Output('date-picker', 'start_date'),
    Output('date-picker', 'end_date'),
    Input('clear-button', 'n_clicks'),
    prevent_initial_call=True
)
def clear_dates(n_clicks):
    return None, None

@callback(
    Output('output', 'children'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_output(start_date, end_date):
    output_string = ''
    
    if start_date == end_date:
        output_string += f'Single Date selected: {start_date}<br>'
    else:
        output_string += f'Date Range selected: {start_date} to {end_date}'
    
    return html.Div([html.Br(), html.Br(), html.Div([html.P(output_string)])])
