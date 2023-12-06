import data.mongodb as mongodb
import pandas as pd

## CONNECT TO DB
dbname = mongodb.get_database()

def execute_aggregation(collection, pipeline):
    """Execute a MongoDB aggregation pipeline and return the result.
    
    Parameters:
    ----------
    collection : str
        Name of the collection.
    pipeline : list
        List of stages.
        
    Returns:
    -------
    list of documents
        """
    try:
        return list(dbname[collection].aggregate(pipeline))
    except Exception as e:
        print(f"Error running aggregation: {e}")
        return []


def build_pipeline(unwind_field=None, match_conditions=None, group_conditions=None, sort_conditions=None, project_conditions=None, replace_root_conditions=None):
    """Build a MongoDB aggregation pipeline with optional stages."""
    pipeline = []

    if unwind_field:
        pipeline.append({"$unwind": unwind_field})
    if match_conditions:
        pipeline.append({"$match": match_conditions})
    if group_conditions:
        pipeline.append({"$group": group_conditions})
    if sort_conditions:
        pipeline.append({"$sort": sort_conditions})
    if project_conditions:
        pipeline.append({"$project": project_conditions})
    if replace_root_conditions:
        pipeline.append({"$replaceRoot": {"newRoot": replace_root_conditions}})

    return pipeline

def get_data(collection, unwind_field=None, match_conditions=None, group_conditions=None, sort_conditions=None, project_conditions=None, replace_root_conditions=None):
    """Get data from a collection using a flexible aggregation pipeline.

    Parameters:
    ----------
    collection : str
        Name of the collection.
    unwind_field : str (optional)
        Field to unwind.
    match_conditions : dict (optional)
        Conditions for the match stage.
    group_conditions : dict (optional)
        Conditions for the group stage.
    sort_conditions : dict (optional)
        Conditions for the sort stage.
    project_conditions : dict (optional)
        Conditions for the project stage.
    replace_root_conditions : dict (optional)
        Conditions for the replaceRoot stage.

    Returns:
    -------
    list
        List of documents resulting from the aggregation.
    """
    pipeline = build_pipeline(unwind_field, match_conditions, group_conditions, sort_conditions, project_conditions, replace_root_conditions)
    return execute_aggregation(collection, pipeline)


def get_data_group_by_sum(collection: str, group_field: str, sum_fields: [str], order: int):
    """ Enable User to get the sum of a field from a collection grouped by a field
    
    Parameters:
    ----------
    collection : str
        Name of the collection.
    group_field : str
        Field to group by.
    sum_fields : [str]
        Fields to sum.
        
    Returns:
    -------
    list
        List of documents.
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
    return execute_aggregation(collection, pipeline)


def get_data_from_one_date(collection: str, date: str):
    """ Enable User to get the data from a collection for a specific date
    
    Parameters:
    ----------
    collection : str
        Name of the collection.
    date : str
        Date.
        
    Returns:
    -------
    list
        List of documents.
    """
    pipeline = [
        {"$unwind": "$results"},
        {"$match": {"results.date": date}},
        {"$replaceRoot": {"newRoot": "$results"}},
        {"$sort": {"date_heure": 1}}
    ]
    return execute_aggregation(collection, pipeline)


def get_data_from_one_date_and_one_region(collection: str, date: str, region: str):
    """ Enable User to get the data from a collection for a specific date and a specific region
    
    Parameters:
    ----------
    collection : str
        Name of the collection.
    date : str
        Date.
    region : str
        Region.
        
    Returns:
    -------
    list
        List of documents.
    """
    pipeline = [
        {"$unwind": "$results"},
        {"$match": {"results.date": date, "results.libelle_region": region}},
        {"$project": {"_id": 0, "date": "$results.date", "data": "$results.data"}},
        {"$sort": {"results.date_heure": 1}}
    ]
    return execute_aggregation(collection, pipeline)


def get_data_from_one_date_to_another_date(collection: str, date1: str, date2: str):
    """Get data from a collection for a specific date range using the modular get_data function.
    
    Parameters:
    ----------
    collection : str
        Name of the collection.
    date1 : str
        Start date for the range.
    date2 : str
        End date for the range.

    Returns:
    -------
    list
        List of documents in the specified date range.
    """
    # Define the match conditions to filter documents between two dates
    match_conditions = {"results.date": {"$gte": date1, "$lte": date2}}

    # Call the get_data function with the match conditions
    return get_data(collection, unwind_field="$results", match_conditions=match_conditions, replace_root_conditions="$results", sort_conditions={"date_heure": 1})


def get_data_from_one_date_to_another_date_and_one_region(collection: str, date1: str, date2: str, region: str):
    """ Enable User to get the data from a collection for a specific date range and a specific region
    
    Parameters:
    ----------
    collection : str
        Name of the collection.
    date1 : str
        First date.
    date2 : str
        Second date.
    region : str
        Region.
        
    Returns:
    -------
    list
        List of documents.
    """
    pipeline = [
        {"$unwind": "$results"},
        {"$match": {"results.date": {"$gte": date1, "$lte": date2}, "results.libelle_region": region}},
        {"$project": {"_id": 0, "date": "$results.date", "data": "$results.data"}},
        {"$sort": {"results.date_heure": 1}}
    ]
    return execute_aggregation(collection, pipeline)


def get_mean_by_date_from_one_date_to_another_date(collection: str, date1: str, date2: str, mean_fields: [str]):
    """ Enable User to get the mean of a field from a collection for a specific date range
    
    Parameters:
    ----------
    collection : str
        Name of the collection.
    date1 : str
        First date.
    date2 : str
        Second date.
    mean_fields : [str]
        Fields to average.
    
    Returns:
    -------
    list
        List of documents.
    """
    pipeline = [
        {"$unwind": "$results"},
        {"$match": {"results.date": {"$gte": date1, "$lte": date2}}},
        {"$replaceRoot": {"newRoot": "$results"}},
        {"$group": {"_id": "$date", **{field: {"$avg": f"$data.{field}"} for field in mean_fields}}},
        {"$sort": {"_id": 1}}
    ]
    return execute_aggregation(collection, pipeline)


def get_average_values(collection, fields):
    """Enable User to get the averages of many fields (when values are not null) from a collection
    
    Parameters:
    ----------
    collection : str
        Name of the collection.
    fields : list of str
        Fields.
        
    Returns:
    -------
    dict
        Dictionary of averages.
    """
    # Construct the match conditions to exclude null and ensure the field exists and is of a numeric type
    match_conditions = {"$and": [{f"results.{field}": {"$ne": None, "$exists": True, "$type": ["double", "int", "long", "decimal"]}} for field in fields]}

    pipeline = [
        {"$unwind": "$results"},
        {"$match": match_conditions},
        {"$group": {"_id": None, **{f"{field}": {"$avg": f"$results.{field}"} for field in fields}}},
        {"$project": {"_id": 0, **{f"{field}": 1 for field in fields}}}
    ]
    result = execute_aggregation(collection, pipeline)
    return result[0] if result else {}


def get_sum_values(collection, fields):
    """Enable User to get the sum of many fields (when values are not null) from a collection
    
    Parameters:
    ----------
    collection : str
        Name of the collection.
    fields : list of str
        Fields.
        
    Returns:
    -------
    dict
        Dictionary of sums.
    """
    # Construct the match conditions to exclude null and ensure the field exists and is of a numeric type
    match_conditions = {"$and": [{f"results.{field}": {"$ne": None, "$exists": True, "$type": ["double", "int", "long", "decimal"]}} for field in fields]}

    pipeline = [
        {"$unwind": "$results"},
        {"$match": match_conditions},
        {"$group": {"_id": None, **{f"{field}": {"$sum": f"$results.{field}"} for field in fields}}},
        {"$project": {"_id": 0, **{f"{field}": 1 for field in fields}}}
    ]
    result = execute_aggregation(collection, pipeline)
    return result[0] if result else {}

def transform_data_to_df(data: list) -> pd.DataFrame:
    """Transform a list of documents to a DataFrame.
    
    Parameters
    ----------
    data : list
        List of documents.
        
    Returns
    -------
    pd.DataFrame
        DataFrame containing the data.
    """
    return pd.DataFrame(data)