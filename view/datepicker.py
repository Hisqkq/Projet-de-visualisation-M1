from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import datetime

year_options = [{'label': i, 'value': i} for i in range(2013, datetime.datetime.now().year + 1)]

# Define the default start and end dates
default_start_date = '2020-01-01'
default_end_date = '2020-01-01'

datepicker = html.Div([
    dcc.Dropdown(id='year-dropdown', options=year_options, placeholder='Select Year'),
    dcc.DatePickerRange(
        id='date-picker',
        start_date=default_start_date,
        end_date=default_start_date,
        end_date_placeholder_text='End Date',
        max_date_allowed= datetime.datetime.now().strftime('%Y-%m-%d'),
        min_date_allowed= "2013-01-01",
    ),
    html.Button('Clear', id='clear-button', n_clicks=0, className='btn btn-primary'),
    html.Div(id='n-clicks-store', style={'display': 'none'}),
])

@callback(
    Output('date-picker', 'start_date'),
    Output('date-picker', 'end_date'),
    Output('year-dropdown', 'value'),
    Output('n-clicks-store', 'children'),
    Input('year-dropdown', 'value'),
    Input('clear-button', 'n_clicks'),
    State('n-clicks-store', 'children'),
)
def update_dates(year, n_clicks, n_clicks_store):
    if n_clicks_store is None:
        n_clicks_store = 0
    if n_clicks > n_clicks_store:
        return None, None, None, n_clicks
    elif year:
        start_date = datetime.date(year, 1, 1)
        return start_date.strftime('%Y-%m-%d'), None, year, n_clicks
    else:
        return None, None, None, n_clicks