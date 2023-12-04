import plotly.express as px
import data.db_services as dbs

import view.map

#### data used by graphs ####

prodution = dbs.get_data_group_by_sum("DonneesRegionales", "date_heure", ["consommation", "ech_physiques", "eolien", "hydraulique", "nucleaire", "solaire"], 1)
test_data_one_date = dbs.get_data_from_one_date("DonneesRegionales", "2013-01-12")
données_echanges = dbs.get_data_from_one_date("DonneesNationales", "2020-07-02")


#### graphs ####

def build_map(scope: str = 'France') -> px.choropleth:
    """Create a map.

    Parameters
    ----------
    scope : str, optional
        Scope of the map, by default 'France'. Can be 'France' or a region.
    
    Returns
    -------
    px.choropleth
        Figure containing the map.
    
    """
    data = view.map.get_json()
    data = view.map.exclude_overseas_and_corsica(data)
    if scope != 'France':
        fig = view.map.build_region_map(data, scope)
    else:
        fig = view.map.build_metropolitan_map(data)
    return fig

line_chart = px.line(prodution, x="_id", y="solaire", labels={
                     "_id": "date_heure",
                     "solaire": "Production solaire",
                 },
                title="Production d'enérgie solaire en France")

line_chart_cons = px.bar(données_echanges, x="date_heure", y="consommation")


def build_stacked_area_chart(data, argument):
    return px.area(data, x="date_heure", y=str(argument), color="libelle_region", title=f"Production {argument}")


def build_stacked_bar_chart(data, arguments):
    return px.bar(data, x="date_heure", y=arguments)

stacked_area_chart_echanges = px.bar(données_echanges, x="date_heure", y=["ech_comm_angleterre", "ech_comm_espagne", "ech_comm_italie", "ech_comm_suisse"])
