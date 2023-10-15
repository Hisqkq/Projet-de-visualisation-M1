"""
Python script that allow the user to fill the database for the first time. 
"""
import api_service
import db_manager
import datetime
import time


def insert_data(collection_name:str, start_date:str, end_date:datetime):
    """Permet de remplir une base de donnée jours par jours 100 lignes par 100 ligne

    Args:
        collection_name (str): nom de la collection 
        start_date (str): date de départ (api_service.get_first_date(collection_name))
        end_date (datetime): dernière date dans le dataframe
    """
    step = 100
    
    current_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = end_date
    
    while current_date <= end_date:
        lines_per_date = api_service.get_length_per_date('eco2mix-regional-tr', str(current_date))
        formatted_date = current_date.strftime('%Y-%m-%d') 
        print(formatted_date)
        
        for i in range(0, lines_per_date, step):
            rows = min(step, lines_per_date - i)
            try:
                data = api_service.fetch_eco2mix(i, rows, str(formatted_date))
                
                if isinstance(data, list):
                    db_manager.insert_many_in_coll(collection_name, data)
                else:
                    db_manager.insert_one_in_coll(collection_name, data)
                    
            except Exception as e:
                print(f"Erreur lors de l'insertion des données pour la date {formatted_date}, offset {i}: {e}")
                print("Réessai dans 5 secondes...")
                time.sleep(5)  
                i -= step  
                continue
                
        current_date += datetime.timedelta(days=1)
        
        
db_manager.create_collection("eco2mix")
insert_data("eco2mix", api_service.get_first_date("eco2mix-regional-tr"), datetime.datetime.now())