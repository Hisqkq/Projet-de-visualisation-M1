import data.mongodb as mongodb
import pandas as pd

## CONNECT TO DB
dbname = mongodb.get_database()

def execute_aggregation(collection: str, pipeline: list) -> list:
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


def build_pipeline(unwind_sector=None, match_conditions=None, group_conditions=None, sort_conditions=None, project_conditions=None, replace_root_conditions=None) -> list:
    """Build a MongoDB aggregation pipeline with optional stages."""
    pipeline = []

    if unwind_sector: pipeline.append({"$unwind": unwind_sector})
    if match_conditions: pipeline.append({"$match": match_conditions})
    if group_conditions: pipeline.append({"$group": group_conditions})
    if sort_conditions: pipeline.append({"$sort": sort_conditions})
    if project_conditions: pipeline.append({"$project": project_conditions})
    if replace_root_conditions: pipeline.append({"$replaceRoot": {"newRoot": replace_root_conditions}})

    return pipeline

def get_data(collection: str, unwind_sector=None, match_conditions=None, group_conditions=None, sort_conditions=None, project_conditions=None, replace_root_conditions=None) -> list:
    """Get data from a collection using a flexible aggregation pipeline.

    Parameters:
    ----------
    collection : str
        Name of the collection.
    unwind_sector : str (optional)
        Sector to unwind.
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
    pipeline = build_pipeline(unwind_sector, match_conditions, group_conditions, sort_conditions, project_conditions, replace_root_conditions)
    return execute_aggregation(collection, pipeline)


def get_data_group_by_sum(collection: str, group_sector: str, sum_sectors: [str], order: int) -> list:
    """Enable User to get the sum of sectors from a collection, grouped by a specific sector.
    
    Parameters:
    ----------
    collection : str
        Name of the collection.
    group_sector : str
        Sector to group by.
    sum_sectors : list of str
        Sectors to sum.
    order : int
        Sorting order (1 for ascending, -1 for descending).

    Returns:
    -------
    list
        List of aggregated documents.
    """
    group_conditions = {
        "_id": f"$results.{group_sector}",
        **{sector: {"$sum": f"$results.{sector}"} for sector in sum_sectors}
    }
    sort_conditions = {"_id": order}
    return get_data(collection, 
                    unwind_sector="$results", 
                    group_conditions=group_conditions, 
                    sort_conditions=sort_conditions)


def get_data_from_one_date(collection: str, date: str) -> list:
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
                    unwind_sector="$results", 
                    match_conditions=match_conditions, 
                    replace_root_conditions="$results", 
                    sort_conditions={"date_heure": 1})


def get_data_from_one_date_and_one_region(collection: str, date: str, region: str) -> list:
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
                    unwind_sector="$results", 
                    match_conditions=match_conditions, 
                    project_conditions=project_conditions, 
                    sort_conditions={"results.date_heure": 1})



def get_data_from_one_date_to_another_date(collection: str, date1: str, date2: str) -> list:
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
                    unwind_sector="$results", 
                    match_conditions=match_conditions, 
                    replace_root_conditions="$results", 
                    sort_conditions={"date_heure": 1})


def get_data_from_one_date_to_another_date_and_one_region(collection: str, date1: str, date2: str, region: str) -> list:
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
                    unwind_sector="$results", 
                    match_conditions=match_conditions, 
                    project_conditions=project_conditions, 
                    sort_conditions={"results.date_heure": 1})


def get_mean_for_sectors(collection: str, date1: str, date2: str, mean_sectors: [str]) -> list:
    """Enable User to get the mean of sectors from a collection for a specific date range.
    
    Parameters:
    ----------
    collection : str
        Name of the collection.
    date1 : str
        Start date for the range.
    date2 : str
        End date for the range.
    mean_sectors : list of str
        Sectors for which to calculate the average.
    
    Returns:
    -------
    list
        List of documents with average values for the specified sectors.
    """
    match_conditions = {"results.date": {"$gte": date1, "$lte": date2}}
    group_conditions = {
        "_id": "$date",
        **{f"{sector}": {"$avg": f"$results.{sector}"} for sector in mean_sectors}
    }
    project_conditions = {"_id": 0, **{f"{sector}": 1 for sector in mean_sectors}}
    return get_data(collection, 
                    unwind_sector="$results", 
                    match_conditions=match_conditions, 
                    group_conditions=group_conditions, 
                    project_conditions=project_conditions,
                    sort_conditions={"_id": 1})

def get_mean_for_sectors_in_a_region(collection: str, date1: str, date2: str, mean_sectors: [str], region: str) -> list:
    """Enable User to get the mean of sectors from a collection for a specific date range and a specific region.
    
    Parameters:
    ----------
    collection : str
        Name of the collection.
    date1 : str
        Start date for the range.
    date2 : str
        End date for the range.
    mean_sectors : list of str
        Sectors for which to calculate the average.
    region : str
        Specific region.
    
    Returns:
    -------
    list
        List of documents with average values for the specified sectors and region.
    """
    match_conditions = {
        "results.date": {"$gte": date1, "$lte": date2},
        "results.libelle_region": region
    }
    group_conditions = {
        "_id": "$date",
        **{f"{sector}": {"$avg": f"$results.{sector}"} for sector in mean_sectors}
    }
    project_conditions = {"_id": 0, **{f"{sector}": 1 for sector in mean_sectors}}
    return get_data(collection, 
                    unwind_sector="$results", 
                    match_conditions=match_conditions, 
                    group_conditions=group_conditions, 
                    project_conditions=project_conditions,
                    sort_conditions={"_id": 1})


def get_average_values(collection: str, sectors: [str]) -> dict:
    """Enable User to get the averages of many sectors (when values are not null) from a collection.
    
    Parameters:
    ----------
    collection : str
        Name of the collection.
    sectors : list of str
        Sectors to calculate the average.
        
    Returns:
    -------
    dict
        Dictionary of averages for each sector.
    """
    match_conditions = {"$and": [{f"results.{sector}": {"$ne": None, "$exists": True, "$type": ["double", "int", "long", "decimal"]}} for sector in sectors]}
    group_conditions = {
        "_id": None, 
        **{f"avg_{sector}": {"$avg": f"$results.{sector}"} for sector in sectors}
    }
    project_conditions = {"_id": 0, **{f"avg_{sector}": 1 for sector in sectors}}
    result = get_data(collection, 
                    unwind_sector="$results", 
                    match_conditions=match_conditions, 
                    group_conditions=group_conditions,
                    project_conditions=project_conditions)
    return result[0] if result else {}

def get_max_value(collection: str, sector: str, columns: [str]) -> dict:
    """Enable User to get the max value of a sector and its corresponding data (columns) from a collection.

    Parameters:
    ----------
    collection : str
        Name of the collection.
    sector : str
        Sector to check.
    columns : list of str
        Columns to return.

    Returns:
    -------
    dict
        Dictionary of the max value and its corresponding data.
    """
    match_conditions = {f"results.{sector}": {"$ne": None, "$exists": True, "$type": ["double", "int", "long", "decimal"]}}
    sort_conditions = {f"results.{sector}": -1}
    project_conditions = {"_id": 0, **{f"results.{column}": 1 for column in columns}}
    result = get_data(collection, 
                    unwind_sector="$results", 
                    match_conditions=match_conditions, 
                    sort_conditions=sort_conditions,
                    project_conditions=project_conditions)
    return result[0] if result else {}



def get_sum_values(collection: str, sectors: [str]) -> dict:
    """Enable User to get the sum of many sectors (when values are not null) from a collection.
    
    Parameters:
    ----------
    collection : str
        Name of the collection.
    sectors : list of str
        Sectors to calculate the sum.
        
    Returns:
    -------
    dict
        Dictionary of sums for each sector.
    """
    match_conditions = {"$and": [{f"results.{sector}": {"$ne": None, "$exists": True, "$type": ["double", "int", "long", "decimal"]}} for sector in sectors]}
    group_conditions = {
        "_id": None, 
        **{f"sum_{sector}": {"$sum": f"$results.{sector}"} for sector in sectors}
    }
    project_conditions = {"_id": 0, **{f"sum_{sector}": 1 for sector in sectors}}
    result = get_data(collection, 
                    unwind_sector="$results", 
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

def remove_nan_from_data(data: pd.DataFrame, column: str) -> pd.DataFrame:
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

def get_last_date_db() -> str:
    """Get the last date in the database. Take the earliest date between the national and regional data.
    
    Returns
    -------
    str
        Date.
    """
    pipeline = [
        {"$unwind": "$results"},
        {"$sort": {"results.date": -1}},
        {"$limit": 1},
        {"$project": {"_id": 0, "date": "$results.date"}}
    ]
    national_result = list(dbname.get_collection("DonneesNationales").aggregate(pipeline))
    regional_result = list(dbname.get_collection("DonneesRegionales").aggregate(pipeline))

    last_national_date = national_result[0]['date'] if national_result else None
    last_regional_date = regional_result[0]['date'] if regional_result else None

    return last_national_date if last_national_date < last_regional_date else last_regional_date

def get_mean_consommation_by_region(collection: str, date1: str, date2: str) -> dict:
    """Enable User to get the mean of consommation by regions from a collection for a specific date range.
    
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
    dict
        Dictionary of mean values for each region.
    """
    pipeline = [
        {"$unwind": "$results"},
        {"$match": {"results.date": {"$gte": date1, "$lte": date2}}},
        {"$group": {
            "_id": "$results.libelle_region",
            "mean_consommation": {"$avg": "$results.consommation"}
        }},
        {"$project": {
            "_id": 0,
            "region": "$_id",
            "mean_consommation": 1
        }},
        {"$sort": {"region": 1}}
    ]

    mean_cons = list(dbname[collection].aggregate(pipeline))
    
    mean_cons_formatted = [
        {"region": data["region"], "mean_consommation": data["mean_consommation"]}
        for data in mean_cons
    ]
    
    mean_cons_dict = {d['region']: d['mean_consommation'] for d in mean_cons_formatted}
    
    return mean_cons_dict
    
    