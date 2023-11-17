import db_constructor

db_constructor.create_collection("eco2mix")
db_constructor.insert_data("eco2mix", db_constructor.get_first_date("eco2mix-regional-tr"), db_constructor.get_last_date("eco2mix-regional-tr"))
db_constructor.create_collection("eco2mix_def")
db_constructor.insert_data("eco2mix-regional-cons-def", "eco2mix_def", db_constructor.get_first_date("eco2mix-regional-cons-def"), db_constructor.get_last_date("eco2mix-regional-cons-def"))
