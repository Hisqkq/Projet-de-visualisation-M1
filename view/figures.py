import configparser
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import data.db_services as dbs
from view.datepicker import default_start_date, default_end_date

### Data ###
# Read the configuration file
config = configparser.ConfigParser()
config.read('data/config.ini')

# Create a dictionary containing the colors for each field
field_colors = {field: config['FieldColorPalette'][field] for field in config['FieldColorPalette']}
exchange_colors = {exchange: config['ExchangeColorPalette'][exchange] for exchange in config['ExchangeColorPalette']}
exchange_colors_bar = {exchange.title(): config['ExchangeColorPaletteBar'][exchange] for exchange in config['ExchangeColorPaletteBar']}
display_names = {name: config['DisplayNameEch'][name] for name in config['DisplayNameEch']}
background_color = str(config['Colors']['background'])
############

## Echanges ##
def build_stacked_bar_chart(arguments: list, 
                            starting_date: str = default_start_date, 
                            ending_date: str = default_end_date) -> px.bar:
    """Create a stacked bar chart.
    
    Parameters
    ----------
    arguments : list
        List of arguments.
    starting_date : str, optional
        Starting date, by default default_start_date.
    ending_date : str, optional
        Ending date, by default default_end_date.
        
    Returns
    -------
    plotly.graph_objects.Figure
        Figure containing the stacked bar chart."""
    
    # Fetching data and converting JSON to DataFrame
    json_data = dbs.get_data_from_one_date_to_another_date("DonneesNationales", starting_date, ending_date)
    data = dbs.transform_data_to_df(json_data)
    data = dbs.convert_to_numeric(data, arguments) # Convert columns to numeric (because some values are strings)
    
    # Check if the necessary columns are in the DataFrame
    if not all(arg in data.columns for arg in arguments):
        raise ValueError("One or more specified arguments are not in the data")
    
    data_renamed = data.rename(columns=display_names)

    data_melted = data_renamed.melt(id_vars='date_heure', value_vars=list(display_names.values()), var_name='Pays', value_name='Echange (MW)') # Melt the DataFrame

    data_melted = data_melted[data_melted['Echange (MW)'] != 0] # Remove rows with 0 value

    fig = px.bar(data_melted, x='date_heure', y='Echange (MW)', color='Pays', 
                 color_discrete_map=exchange_colors_bar, barmode='relative', template="plotly_dark",
                 custom_data=['Pays'])

    fig.update_layout(bargroupgap=0.05)
    fig.update_traces(marker_line_width=0)
    fig.update_layout(paper_bgcolor= background_color)
    fig.update_layout(font_color= "#FFFFFF")
    fig.update_layout(hovermode="x unified")
    fig.update_traces(hovertemplate="%{y:.2f} MW<br>Date: %{x|%Y-%m-%d %H:%M}")
    
    return fig

def build_boxplot_echanges(starting_date: str = default_start_date, ending_date: str = default_end_date):
    """Create a boxplot chart for each exchange.
    
    Parameters
    ----------
    starting_date : str, optional
        Starting date, by default default_start_date.
    ending_date : str, optional
        Ending date, by default default_end_date.
        
    Returns
    -------
    plotly.graph_objects.Figure
        Figure containing the boxplot."""
    
    # Fetching data and converting JSON to DataFrame
    json_data = dbs.get_data_from_one_date_to_another_date("DonneesNationales", starting_date, ending_date)
    data = dbs.transform_data_to_df(json_data)
    data = dbs.convert_to_numeric(data, ["ech_comm_angleterre", "ech_comm_espagne", "ech_comm_italie", "ech_comm_suisse", "ech_comm_allemagne_belgique"])
    
    if not all(arg in data.columns for arg in ["ech_comm_angleterre", "ech_comm_espagne", "ech_comm_italie", "ech_comm_suisse", "ech_comm_allemagne_belgique"]):
        raise ValueError("One or more specified arguments are not in the data")
    
    data_renamed = data.rename(columns=display_names)

    melted_data = data_renamed.melt(value_vars=list(display_names.values()), 
                                    var_name='Pays', value_name='Echange (MW)')
    
    melted_data = melted_data[melted_data['Echange (MW)'] != 0]

    fig = px.box(melted_data, y='Echange (MW)', x='Pays', color='Pays',
                template="plotly_dark", color_discrete_map=exchange_colors_bar)

    fig.update_layout(paper_bgcolor= background_color, font_color="#FFFFFF")

    return fig

def build_donuts_exchanges(starting_date: str = default_start_date, ending_date: str = default_end_date):
    """Create a donut chart.

    Parameters
    ----------
    starting_date : str, optional
        Starting date, by default default_start_date.
    ending_date : str, optional
        Ending date, by default default_end_date.

    Returns
    -------
    plotly.graph_objects.Figure
        Figure containing the donut chart.
    """
    json_data = dbs.get_data_from_one_date_to_another_date("DonneesNationales", starting_date, ending_date)
    data = dbs.transform_data_to_df(json_data)
    data = dbs.convert_to_numeric(data, ["ech_comm_angleterre", "ech_comm_espagne", "ech_comm_italie", "ech_comm_suisse", "ech_comm_allemagne_belgique"])
    
    columns = ['ech_comm_angleterre', 'ech_comm_espagne', 'ech_comm_italie', 'ech_comm_suisse', 'ech_comm_allemagne_belgique']
    data = data[data.columns.intersection(columns)]

    imports = data[data > 0].fillna(0).sum()
    exports = -data[data < 0].fillna(0).sum()

    import_labels = [display_names.get(col, col) for col in imports.index]
    export_labels = [display_names.get(col, col) for col in exports.index]

    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])

    def hex_to_rgba(hex, alpha=0.7):
        """Convert hex color to rgba format with specified alpha."""
        hex = hex.lstrip('#')
        return f"rgba({int(hex[0:2], 16)}, {int(hex[2:4], 16)}, {int(hex[4:6], 16)}, {alpha})"

    import_colors = [exchange_colors.get(label, '#FFFFFF') for label in imports.index]
    export_colors = [exchange_colors.get(label, '#FFFFFF') for label in exports.index]

    import_colors_transparent = [hex_to_rgba(c) for c in import_colors]
    export_colors_transparent = [hex_to_rgba(c) for c in export_colors]

    if not imports.empty:
        fig.add_trace(go.Pie(labels=import_labels, values=imports, marker=dict(colors=import_colors_transparent, line=dict(color=import_colors, width=2)), name='Imports', hole=.4, textfont=dict(color='#FFFFFF')), 1, 1)
    if not exports.empty:
        fig.add_trace(go.Pie(labels=export_labels, values=exports, marker=dict(colors=export_colors_transparent, line=dict(color=export_colors, width=2)), name='Exports', hole=.4, textfont=dict(color='#FFFFFF')), 1, 2)

    fig.update_traces(textinfo='percent+label')
    fig.update_layout(paper_bgcolor=background_color, font_color="#FFFFFF") 
    fig.update_layout(annotations=[dict(text='Imports', x=0.17, y=0.5, font_size=20, showarrow=False), dict(text='Exports', x=0.832, y=0.5, font_size=20, showarrow=False)])

    return fig

## Production ##
def build_stacked_area_chart(argument: str = "nucleaire", 
                             starting_date: str = default_start_date, 
                             ending_date: str = default_end_date,
                             homepage:bool=False) -> px.area:
    """Create a stacked area chart for one production fiels.
    
    Parameters
    ----------
    argument : str, optional
        Argument (production field), by default "nucleaire".
    date : str, optional
        Date, by default datetime.datetime.now().strftime("%Y-%m-%d").
    homepage : bool, optional
        True if the stacked area chart is for the homepage, False otherwise, by default False.
        
    Returns
    -------
    plotly.graph_objects.Figure
        Figure containing the stacked area chart."""
    data = dbs.get_data_from_one_date_to_another_date("DonneesRegionales", starting_date, ending_date)
    fig = px.area(data, x="date_heure", y=str(argument), color="libelle_region", title=f"Production {argument}", template="plotly_dark")
    if not homepage:
        fig.update_layout(paper_bgcolor=background_color)
        fig.update_layout(font_color="#FFFFFF") 
    return fig

def build_stacked_area_by_production(starting_date: str = default_start_date, 
                                     ending_date: str = default_end_date,):
    """Create a stacked area chart for each production field.
    
    Parameters
    ----------
    starting_date : str
        Starting date.
    end_date : str
        Ending date.
        
    Returns
    -------
    plotly.graph_objects.Figure
        Figure containing the stacked area chart."""
    data = dbs.transform_data_to_df(dbs.get_data_from_one_date_to_another_date("DonneesNationales", starting_date, ending_date))
    data = data.sort_values(by=['date_heure'])
    data = dbs.remove_nan_from_data(data, "consommation")
    
    production_fields = ["eolien", "hydraulique", "nucleaire", "solaire", "bioenergies", "gaz", "fioul", "charbon"]
    if not set(production_fields).issubset(data.columns):
        missing_fields = list(set(production_fields) - set(data.columns))
        raise ValueError(f"Les colonnes suivantes sont manquantes dans le DataFrame: {missing_fields}")

    fig = px.area(data, x="date_heure", y=production_fields, title="Production par filière", color_discrete_map=field_colors, template="plotly_dark")
    fig.update_layout(paper_bgcolor=background_color)
    fig.update_layout(font_color="#FFFFFF") 
    return fig

## Consommation ##
def build_line_chart_with_prediction(starting_date: str = default_start_date, 
                                     ending_date: str = default_end_date, 
                                     homepage:bool=False) -> px.area:
    """Create a line chart.
    
    Parameters
    ----------
    starting_date : str, optional
        Starting date, by default default_start_date.
    ending_date : str, optional
        Ending date, by default default_end_date.
    homepage : bool, optional
        True if the line chart is for the homepage, False otherwise, by default False.
        
    Returns
    -------
    plotly.graph_objects.Figure
        Figure containing the line chart.
    """
    # Fetching data and converting JSON to DataFrame
    json_data = dbs.get_data_from_one_date_to_another_date("DonneesNationales", starting_date, ending_date)
    data = dbs.transform_data_to_df(json_data)
    #Order data by datetime
    data = data.sort_values(by=['date_heure'])
    data = dbs.remove_nan_from_data(data, "consommation")

    # Check if the necessary columns are in the DataFrame
    if not {'date_heure', 'consommation', 'prevision_j', 'prevision_j1'}.issubset(data.columns):
        raise ValueError("One or more required columns are missing in the data")

    # Creating the line chart
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data["date_heure"], y=data["consommation"], fill='tozeroy', mode='none', name='Consommation'))
    fig.add_trace(go.Scatter(x=data["date_heure"], y=data["prevision_j"], mode='lines', name='Prediction J'))
    fig.add_trace(go.Scatter(x=data["date_heure"], y=data["prevision_j1"], mode='lines', name='Prediction J-1'))

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        xanchor="center",
        y = 1.2,
        x = 0.5
    ))
    fig.update_layout(title="Consommation nationale avec prédictions", template="plotly_dark", hovermode="x unified")
    fig.update_yaxes(title_text="Consommation (MW)")
    fig.update_xaxes(title_text="Date/Heure")
    fig.update_traces(hovertemplate="%{y:.2f} MW<br>Date: %{x|%Y-%m-%d %H:%M}")

    if not homepage:
        fig.update_layout(paper_bgcolor=background_color)
        fig.update_layout(font_color="#FFFFFF")

    return fig

def build_line_chart_consommation_by_region(starting_date: str = default_start_date, 
                                            ending_date: str = default_end_date, 
                                            homepage:bool=False) -> px.line:
    """Create a line chart.
    
    Parameters
    ----------
    starting_date : str, optional
        Starting date, by default default_start_date.
    ending_date : str, optional
        Ending date, by default default_end_date.
    homepage : bool, optional
        True if the line chart is for the homepage, False otherwise, by default False.
        
    Returns
    -------
    plotly.graph_objects.Figure
        Figure containing the line chart.
    """
    # Fetching data and converting JSON to DataFrame
    json_data = dbs.get_data_from_one_date_to_another_date("DonneesRegionales", starting_date, ending_date)
    data = dbs.transform_data_to_df(json_data)
    #Order data by datetime
    data = data.sort_values(by=['date_heure'])
    data = dbs.remove_nan_from_data(data, "consommation")

    # Check if the necessary columns are in the DataFrame
    if not {'date_heure', 'consommation', 'libelle_region'}.issubset(data.columns):
        raise ValueError("One or more required columns are missing in the data")

    # Creating the line chart
    line_chart_cons = px.line(data, x="date_heure", y="consommation", color="libelle_region", template="plotly_dark", title="Consommation par région")
    line_chart_cons.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        xanchor="center",
        y = 1.2,
        x = 0.5
    ))

    if not homepage:
        line_chart_cons.update_layout(paper_bgcolor=background_color)
        line_chart_cons.update_layout(font_color="#FFFFFF")
    
    line_chart_cons.update_yaxes(title_text="Consommation (MW)")
    line_chart_cons.update_xaxes(title_text="Date/Heure")
    line_chart_cons.update_layout(hovermode="x unified")
    line_chart_cons.update_traces(hovertemplate="%{y:.2f} MW<br>Date: %{x|%Y-%m-%d %H:%M}")



    return line_chart_cons