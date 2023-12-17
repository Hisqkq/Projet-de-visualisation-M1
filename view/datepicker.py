from dash import html, callback
from dash.dependencies import Input, Output, State
import datetime
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
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
            dmc.DateRangePicker(
                id="date-range-picker",
                allowSingleDateInRange=True,
                maxDate=datetime.datetime.now().strftime('%Y-%m-%d'),
                minDate=default_min_date_allowed,
                inputFormat="DD-MM-YYYY",
                weekendDays = [None],
                value=[default_start_date, default_end_date],
                amountOfMonths=1,
                style={"width": 230},
                opacity="1"),
        ),
    ]),
])