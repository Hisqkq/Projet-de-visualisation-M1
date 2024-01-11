import mongodb as mongodb
import pandas as pd
import time

import db_services as dbs

project_conditions = {"_id": 0,"results.stockage_batterie":0,"results.destockage_batterie":0,
                        "results.eolien_terrestre":0,"results.eolien_offshore":0, "results.tco_thermique":0,
                        "results.tch_thermique":0,"results.tco_nucleaire":0,"results.tch_nucleaire":0,"results.tco_eolien":0, 
                        "results.tch_eolien":0,"results.tco_solaire":0,"results.tch_solaire":0,"results.tco_hydraulique":0,
                        "results.tch_hydraulique":0, "results.tco_bioenergies":0, "results.tch_bioenergies":0}

####################################################################################################
# test time to get all regional data and transform it to df

time_start = time.time()

regionales_df = dbs.transform_data_to_df(dbs.get_data("DonneesRegionales",
                                                      replace_root_conditions="$results", 
                                                      project_conditions=project_conditions,
                                                      unwind_sector="$results"))

time_end = time.time()

print(f"Temps DonneesRegionales : {time_end - time_start}s") # 125.36566829681396s

###################################################################################################
# test time to get all natioal data and transform it to df

time_start = time.time()

nationales_df = dbs.transform_data_to_df(dbs.get_data("DonneesNationales", 
                                              replace_root_conditions="$results", 
                                              project_conditions=project_conditions,
                                              unwind_sector="$results")) 

time_end = time.time()

print(f"Temps DonneesNationales : {time_end - time_start}s") # 17.678868293762207s

####################################################################################################
# test time to get all regional data from one date to another date using mongodb

time_start = time.time()

regionales_df_date_to_date = dbs.get_data_between_two_dates("DonneesRegionales", "2020-01-01", "2020-01-02")

time_end = time.time()

print(f"Temps DonneesRegionales date to date using mongodb : {time_end - time_start}s") # 22.25581121444702s

####################################################################################################
# test time to get all regional data from one date to another date but using pd

time_start = time.time()

regionales_df_date_to_date = regionales_df[(regionales_df["date"] >= "2020-01-01") & (regionales_df["date"] <= "2020-01-02")]

time_end = time.time()

print(f"Temps DonneesRegionales date to date using pd : {time_end - time_start}s") # 13.114590883255005s

###################################################################################################
# test time to get all national data from one date to another date using mongodb

time_start = time.time()

nationales_df_date_to_date = dbs.get_data_between_two_dates("DonneesNationales", "2020-01-01", "2020-01-02")

time_end = time.time()

print(f"Temps DonneesNationales date to date using mongodb : {time_end - time_start}s") # 3.731673002243042s

####################################################################################################
# test time to get all nationales data from one date to another date but using pd

time_start = time.time()

nationales_df_date_to_date = nationales_df[(nationales_df["date"] >= "2020-01-01") & (nationales_df["date"] <= "2020-01-02")]

time_end = time.time()

print(f"Temps DonneesNationales date to date using pd : {time_end - time_start}s") # 0.2630729675292969s