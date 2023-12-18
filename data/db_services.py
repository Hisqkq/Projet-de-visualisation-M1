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

    if unwind_field: pipeline.append({"$unwind": unwind_field})
    if match_conditions: pipeline.append({"$match": match_conditions})
    if group_conditions: pipeline.append({"$group": group_conditions})
    if sort_conditions: pipeline.append({"$sort": sort_conditions})
    if project_conditions: pipeline.append({"$project": project_conditions})
    if replace_root_conditions: pipeline.append({"$replaceRoot": {"newRoot": replace_root_conditions}})

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
    """Enable User to get the sum of fields from a collection, grouped by a specific field.
    
    Parameters:
    ----------
    collection : str
        Name of the collection.
    group_field : str
        Field to group by.
    sum_fields : list of str
        Fields to sum.
    order : int
        Sorting order (1 for ascending, -1 for descending).

    Returns:
    -------
    list
        List of aggregated documents.
    """
    group_conditions = {
        "_id": f"$results.{group_field}",
        **{field: {"$sum": f"$results.{field}"} for field in sum_fields}
    }
    sort_conditions = {"_id": order}
    return get_data(collection, 
                    unwind_field="$results", 
                    group_conditions=group_conditions, 
                    sort_conditions=sort_conditions)


def get_data_from_one_date(collection: str, date: str):
    """Enable User to get the data from a collection for a specific date.
    
    Parameters:
    ----------
    collection : str
        Name of the collection.
    date : str
        Date for which to get the data.
        
    Returns:
    -------
    list
        List of documents for the specified date.
    """
    match_conditions = {"results.date": date}
    return get_data(collection, 
                    unwind_field="$results", 
                    match_conditions=match_conditions, 
                    replace_root_conditions="$results", 
                    sort_conditions={"date_heure": 1})


def get_data_from_one_date_and_one_region(collection: str, date: str, region: str):
    """Enable User to get the data from a collection for a specific date and a specific region.
    
    Parameters:
    ----------
    collection : str
        Name of the collection.
    date : str
        Specific date.
    region : str
        Specific region.
        
    Returns:
    -------
    list
        List of documents for the specified date and region.
    """
    match_conditions = {"results.date": date, "results.libelle_region": region}
    project_conditions = {"_id": 0, "date": "$results.date", "data": "$results.data"}
    return get_data(collection, 
                    unwind_field="$results", 
                    match_conditions=match_conditions, 
                    project_conditions=project_conditions, 
                    sort_conditions={"results.date_heure": 1})



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
    match_conditions = {"results.date": {"$gte": date1, "$lte": date2}}
    return get_data(collection, 
                    unwind_field="$results", 
                    match_conditions=match_conditions, 
                    replace_root_conditions="$results", 
                    sort_conditions={"date_heure": 1})


def get_data_from_one_date_to_another_date_and_one_region(collection: str, date1: str, date2: str, region: str):
    """Enable User to get the data from a collection for a specific date range and a specific region.
    
    Parameters:
    ----------
    collection : str
        Name of the collection.
    date1 : str
        Start date for the range.
    date2 : str
        End date for the range.
    region : str
        Specific region.
        
    Returns:
    -------
    list
        List of documents for the specified date range and region.
    """
    match_conditions = {
        "results.date": {"$gte": date1, "$lte": date2},
        "results.libelle_region": region
    }
    project_conditions = {"_id": 0, "date": "$results.date", "data": "$results.data"}
    return get_data(collection, 
                    unwind_field="$results", 
                    match_conditions=match_conditions, 
                    project_conditions=project_conditions, 
                    sort_conditions={"results.date_heure": 1})


def get_mean_by_date_from_one_date_to_another_date(collection: str, date1: str, date2: str, mean_fields: [str]):
    """Enable User to get the mean of fields from a collection for a specific date range.
    
    Parameters:
    ----------
    collection : str
        Name of the collection.
    date1 : str
        Start date for the range.
    date2 : str
        End date for the range.
    mean_fields : list of str
        Fields for which to calculate the average.
    
    Returns:
    -------
    list
        List of documents with average values for the specified fields.
    """
    match_conditions = {"results.date": {"$gte": date1, "$lte": date2}}
    group_conditions = {
        "_id": "$date",
        **{f"avg_{field}": {"$avg": f"$results.{field}"} for field in mean_fields}
    }
    project_conditions = {"_id": 0, **{f"avg_{field}": 1 for field in mean_fields}}
    return get_data(collection, 
                    unwind_field="$results", 
                    match_conditions=match_conditions, 
                    group_conditions=group_conditions, 
                    project_conditions=project_conditions,
                    sort_conditions={"_id": 1})



def get_average_values(collection, fields):
    """Enable User to get the averages of many fields (when values are not null) from a collection.
    
    Parameters:
    ----------
    collection : str
        Name of the collection.
    fields : list of str
        Fields to calculate the average.
        
    Returns:
    -------
    dict
        Dictionary of averages for each field.
    """
    match_conditions = {"$and": [{f"results.{field}": {"$ne": None, "$exists": True, "$type": ["double", "int", "long", "decimal"]}} for field in fields]}
    group_conditions = {
        "_id": None, 
        **{f"avg_{field}": {"$avg": f"$results.{field}"} for field in fields}
    }
    project_conditions = {"_id": 0, **{f"avg_{field}": 1 for field in fields}}
    result = get_data(collection, 
                    unwind_field="$results", 
                    match_conditions=match_conditions, 
                    group_conditions=group_conditions,
                    project_conditions=project_conditions)
    return result[0] if result else {}


def get_sum_values(collection, fields):
    """Enable User to get the sum of many fields (when values are not null) from a collection.
    
    Parameters:
    ----------
    collection : str
        Name of the collection.
    fields : list of str
        Fields to calculate the sum.
        
    Returns:
    -------
    dict
        Dictionary of sums for each field.
    """
    match_conditions = {"$and": [{f"results.{field}": {"$ne": None, "$exists": True, "$type": ["double", "int", "long", "decimal"]}} for field in fields]}
    group_conditions = {
        "_id": None, 
        **{f"sum_{field}": {"$sum": f"$results.{field}"} for field in fields}
    }
    project_conditions = {"_id": 0, **{f"sum_{field}": 1 for field in fields}}
    result = get_data(collection, 
                    unwind_field="$results", 
                    match_conditions=match_conditions, 
                    group_conditions=group_conditions,
                    project_conditions=project_conditions)
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

def convert_to_numeric(df: pd.DataFrame, columns: [str]) -> pd.DataFrame:
    """Convert columns to numeric values.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the data.
    columns : list of str
        Columns to convert.
        
    Returns
    -------
    pd.DataFrame
        DataFrame containing the data.
    """
    for column in columns: # Convert columns to numeric values (but some values are NA so we need to convert them to 0)
        df[column] = df[column].fillna(0)
        df[column] = df[column].astype(int)
    return df

def remove_nan_from_data(data, column):
    """Remove NaN values from a column.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing the data.
    column : str
        Column to check.

    Returns
    -------
    pd.DataFrame
        DataFrame containing the data.
    """

    return data[data[column].notna()]