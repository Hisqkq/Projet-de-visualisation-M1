import plotly.express as px
import data.db_services as dbs


#### data used by graphs ####

prodution_nucleaire = dbs.get_data_group_by_sum("DonneesRegionales", "date", ["consommation", "ech_physiques", "eolien", "hydraulique", "nucleaire"], 1)
données_1mars2023 = dbs.get_data_from_one_date("DonneesRegionales", "2022-09-12")


#### graphs ####

fig = px.line(prodution_nucleaire, x="_id", y="nucleaire")
fig2 = px.area(données_1mars2023, x="date_heure", y="nucleaire", color="libelle_region")