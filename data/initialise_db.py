import db_constructor

db_constructor.create_collection("DonneesRegionales")
db_constructor.update_data("eco2mix-regional-tr", "DonneesRegionales")
db_constructor.create_collection("eco2mix_def")
db_constructor.update_data("eco2mix-regional-cons-def", "eco2mix_def")