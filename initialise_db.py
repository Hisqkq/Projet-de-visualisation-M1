import data.db_constructor as db_constructor

# Change to False to initialise the whole database
# True will only download data from the real-time APIs
demo = True

if __name__ == "__main__":
    print("Starting database construction...")
    db_constructor.create_collection("DonneesNationales")
    db_constructor.create_collection("DonneesRegionales")
    db_constructor.perform_update(demo=demo)
    db_constructor.create_indexes()