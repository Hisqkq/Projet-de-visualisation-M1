import db_constructor

print("Starting database construction...")

#### Regional data ####
print("Filling regional data...")
# db_constructor.create_collection("DonneesRegionales")
# db_constructor.update_data("eco2mix-regional-cons-def", "DonneesRegionales")
db_constructor.update_data("eco2mix-regional-tr", "DonneesRegionales")

#### National data ####
print("Filling national data...")
# db_constructor.create_collection("DonneesNationales")
# db_constructor.update_data("eco2mix-national-cons-def", "DonneesNationales")
db_constructor.update_data("eco2mix-national-tr", "DonneesNationales")