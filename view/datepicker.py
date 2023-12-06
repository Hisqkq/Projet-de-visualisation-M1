from dash import dcc, html, callback
from dash.dependencies import Input, Output
import datetime

datepicker = html.Div([
    dcc.DatePickerRange(
        id='date-picker',
        start_date='2020-01-01',
        end_date='2020-01-01',
        end_date_placeholder_text='End Date',
        max_date_allowed= datetime.datetime.now().strftime('%Y-%m-%d'),
        min_date_allowed= "2013-01-01",
    ),
    html.Button('Clear', id='clear-button', n_clicks=0, className='btn btn-primary'),
])

@callback(
    Output('date-picker', 'start_date'),
    Output('date-picker', 'end_date'),
    Input('clear-button', 'n_clicks'),
)
def clear_dates(_):
    return None, None
