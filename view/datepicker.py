from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import datetime
import dash_bootstrap_components as dbc
import configparser

config = configparser.ConfigParser()
config.read('data/config.ini')

### Variables ###
# DatepickerDate
default_start_date = config.get('DatepickerDate', 'default_start_date')
default_end_date = config.get('DatepickerDate', 'default_end_date')
default_min_date_allowed = config.get('DatepickerDate', 'default_min_date_allowed')

# YearDropdown
year_options = [{'label': i, 'value': i} for i in range(2013, datetime.datetime.now().year + 1)]
##################

### Datepicker ###
datepicker = html.Div([
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(id='year-dropdown', 
                         options=year_options, 
                         placeholder='Select Year', 
                         style={'width': '50%'})
        ),
        dbc.Col(
            dcc.DatePickerRange(
                id='date-picker',
                start_date=default_start_date,
                end_date=default_end_date,
                end_date_placeholder_text='End Date',
                max_date_allowed=datetime.datetime.now().strftime('%Y-%m-%d'),
                min_date_allowed=default_min_date_allowed),
        ),
        dbc.Col(
        html.Button('Clear', id='clear-button', n_clicks=0, className='btn btn-primary')
        ),
    ]),
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