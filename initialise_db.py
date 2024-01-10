import data.db_constructor as db_constructor

def perform_update():
    """Update data from RTE's API."""

    #### National data ####
    print("Filling national data...")
    db_constructor.update_data("eco2mix-national-cons-def", "DonneesNationales")
    db_constructor.update_data("eco2mix-national-tr", "DonneesNationales")

    #### Regional data ####
    print("Filling regional data...")
    db_constructor.update_data("eco2mix-regional-cons-def", "DonneesRegionales")
    db_constructor.update_data("eco2mix-regional-tr", "DonneesRegionales")

if __name__ == "__main__":
    print("Starting database construction...")
    db_constructor.create_collection("DonneesNationales")
    db_constructor.create_collection("DonneesRegionales")

    perform_update()