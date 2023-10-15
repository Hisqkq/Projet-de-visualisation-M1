"""
Generate pandas datasets from the database that are going to be use to build the graphics. 
"""

import data.db_manager as db_manager

df_production = db_manager.transform_to_df(db_manager.get_data_group_by_sum("eco2mix", "date", ["consommation", "ech_physiques", "eolien", "hydraulique", "nucleaire"], 1))
