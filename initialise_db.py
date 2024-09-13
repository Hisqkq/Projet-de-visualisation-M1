import data.db_constructor as db_constructor

if __name__ == "__main__":
    print("Starting database construction...")
    db_constructor.create_collection("DonneesNationales")
    db_constructor.create_collection("DonneesRegionales")
    db_constructor.perform_update()
    db_constructor.create_indexes()