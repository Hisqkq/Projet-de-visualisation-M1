from dash import dcc, html, callback
from dash.dependencies import Input, Output

datepicker = html.Div([
    dcc.DatePickerRange(
        id='date-picker',
        start_date='2020-01-01',
        end_date='2020-01-01',
        end_date_placeholder_text='End Date'
    ),
    html.Button('Clear', id='clear-button', n_clicks=0, className='btn btn-primary'),
])

@callback(
    Output('date-picker', 'start_date'),
    Output('date-picker', 'end_date'),
    Input('clear-button', 'n_clicks'),
    prevent_initial_call=True
)
def clear_dates(n_clicks):
    return None, None
