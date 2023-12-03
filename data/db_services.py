import data.mongodb as mongodb
import pandas as pd

## CONNECT TO DB
dbname = mongodb.get_database()


def get_data(collection:str):
    """Enable User to get the raw data of a collection from the database
    
    Args:
        collection (str): collection name

    Returns:
        list: données de la table
    """
    return list(dbname[collection].find())


def get_data_group_by_sum(collection: str, group_field: str, sum_fields: [str], order: int):
    """ Enable User to get the sum of a field from a collection grouped by a field
    Parameters:
    - collection (str): Name of the collection.
    - group_field (str): Field used by the group by operator.
    - sum_fields (list of str): Summed fields.
    - order (int): 1 for ascendant sorting and -1 for descendant sorting.
    
    Returns:
    - list: List of documents.
    """
    pipeline = [
        {"$unwind": "$results"},
        {
            "$group": {
                "_id": f"$results.{group_field}",
                **{field: {"$sum": f"$results.{field}"} for field in sum_fields}
            }
        },
        {"$sort": {"_id": order}}
    ]
    return list(dbname[collection].aggregate(pipeline))


def get_data_from_one_date(collection: str, date: str):
    """ Enable User to get the data from a collection for a specific date"""
    pipeline = [
        {"$unwind": "$results"},
        {"$match": {"results.date": date}},
        {"$replaceRoot": {"newRoot": "$results"}},
        {"$sort": {"date_heure": 1}}
    ]
    return list(dbname[collection].aggregate(pipeline))


def get_data_from_one_date_and_one_region(collection: str, date: str, region: str):
    """ Enable User to get the data from a collection for a specific date and a specific region"""
    pipeline = [
        {"$unwind": "$results"},
        {"$match": {"results.date": date, "results.libelle_region": region}},
        {"$project": {"_id": 0, "date": "$results.date", "data": "$results.data"}},
        {"$sort": {"results.date_heure": 1}}
    ]
    return list(dbname[collection].aggregate(pipeline))


def get_data_from_one_date_to_another_date(collection: str, date1: str, date2: str):
    """ Enable User to get the data from a collection for a specific date range"""
    pipeline = [
        {"$unwind": "$results"},
        {"$match": {"results.date": {"$gte": date1, "$lte": date2}}},
        {"$replaceRoot": {"newRoot": "$results"}},
        {"$sort": {"date_heure": 1}}
    ]
    return list(dbname[collection].aggregate(pipeline))


def get_data_from_one_date_to_another_date_and_one_region(collection: str, date1: str, date2: str, region: str):
    """ Enable User to get the data from a collection for a specific date range and a specific region"""
    pipeline = [
        {"$unwind": "$results"},
        {"$match": {"results.date": {"$gte": date1, "$lte": date2}, "results.libelle_region": region}},
        {"$project": {"_id": 0, "date": "$results.date", "data": "$results.data"}},
        {"$sort": {"results.date_heure": 1}}
    ]
    return list(dbname[collection].aggregate(pipeline))


def get_mean_by_date_from_one_date_to_another_date(collection: str, date1: str, date2: str, mean_fields: [str]):
    """ Enable User to get the mean of a field from a collection for a specific date range"""
    pipeline = [
        {"$unwind": "$results"},
        {"$match": {"results.date": {"$gte": date1, "$lte": date2}}},
        {"$replaceRoot": {"newRoot": "$results"}},
        {"$group": {"_id": "$date", **{field: {"$avg": f"$data.{field}"} for field in mean_fields}}},
        {"$sort": {"_id": 1}}
    ]
    return list(dbname[collection].aggregate(pipeline))