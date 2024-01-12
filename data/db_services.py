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


def build_pipeline(unwind_sector=None,
                   match_conditions=None,
                   group_conditions=None,
                   sort_conditions=None,
                   project_conditions=None,
                   replace_root_conditions=None) -> list:
    """Build a MongoDB aggregation pipeline with optional stages."""
    pipeline = []

    if unwind_sector: pipeline.append({"$unwind": unwind_sector})
    if match_conditions: pipeline.append({"$match": match_conditions})
    if group_conditions: pipeline.append({"$group": group_conditions})
    if sort_conditions: pipeline.append({"$sort": sort_conditions})
    if project_conditions: pipeline.append({"$project": project_conditions})
    if replace_root_conditions:
        pipeline.append({"$replaceRoot": {"newRoot": replace_root_conditions}})

    return pipeline


def get_data(collection: str,
             unwind_sector=None,
             match_conditions=None,
             group_conditions=None,
             sort_conditions=None,
             project_conditions=None,
             replace_root_conditions=None) -> list:
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
    pipeline = build_pipeline(unwind_sector, match_conditions,
                              group_conditions, sort_conditions,
                              project_conditions, replace_root_conditions)
    return execute_aggregation(collection, pipeline)


def get_data_between_two_dates(collection: str,
                               date1: str,
                               date2: str,
                               region: str = None) -> list:
    """Get data from a collection for a specific date range using the modular get_data function.
    
    Parameters:
    ----------
    collection : str
        Name of the collection.
    date1 : str
        Start date for the range.
    date2 : str
        End date for the range.
    region : str (optional)
        Region for which to get the data.

    Returns:
    -------
    list
        List of documents in the specified date range.
    """
    if region:
        match_conditions = {
            "results.date": {
                "$gte": date1,
                "$lte": date2
            },
            "results.libelle_region": region
        }
    else:
        match_conditions = {"results.date": {"$gte": date1, "$lte": date2}}
    return get_data(collection,
                    unwind_sector="$results",
                    match_conditions=match_conditions,
                    replace_root_conditions="$results",
                    sort_conditions={"date_heure": 1})


def get_mean_for_sectors(collection: str,
                         date1: str,
                         date2: str,
                         mean_sectors: [str],
                         region: str = None) -> list:
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
    region : str (optional)
        Region for which to get the data.
    
    Returns:
    -------
    list
        List of documents with average values for the specified sectors.
    """
    group_conditions = {
        "_id": "$date",
        **{
            f"{sector}": {
                "$avg": f"$results.{sector}"
            }
            for sector in mean_sectors
        }
    }
    project_conditions = {
        "_id": 0,
        **{
            f"{sector}": 1
            for sector in mean_sectors
        }
    }
    if region:
        match_conditions = {
            "results.date": {
                "$gte": date1,
                "$lte": date2
            },
            "results.libelle_region": region
        }
    else:
        match_conditions = {"results.date": {"$gte": date1, "$lte": date2}}
    return get_data(collection,
                    unwind_sector="$results",
                    match_conditions=match_conditions,
                    group_conditions=group_conditions,
                    project_conditions=project_conditions,
                    sort_conditions={"_id": 1})


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
    for column in columns:  # Convert columns to numeric values (but some values are NA so we need to convert them to 0)
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
    pipeline = [{
        "$unwind": "$results"
    }, {
        "$sort": {
            "results.date": -1
        }
    }, {
        "$limit": 1
    }, {
        "$project": {
            "_id": 0,
            "date": "$results.date"
        }
    }]
    national_result = list(
        dbname.get_collection("DonneesNationales").aggregate(pipeline))
    regional_result = list(
        dbname.get_collection("DonneesRegionales").aggregate(pipeline))

    last_national_date = national_result[0]['date'] if national_result else None
    last_regional_date = regional_result[0]['date'] if regional_result else None

    return last_national_date if last_national_date < last_regional_date else last_regional_date


def get_mean_consommation_by_region(collection: str, date1: str,
                                    date2: str) -> dict:
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
    pipeline = [{
        "$unwind": "$results"
    }, {
        "$match": {
            "results.date": {
                "$gte": date1,
                "$lte": date2
            }
        }
    }, {
        "$group": {
            "_id": "$results.libelle_region",
            "mean_consommation": {
                "$avg": "$results.consommation"
            }
        }
    }, {
        "$project": {
            "_id": 0,
            "region": "$_id",
            "mean_consommation": 1
        }
    }, {
        "$sort": {
            "region": 1
        }
    }]

    mean_cons = list(dbname[collection].aggregate(pipeline))

    mean_cons_formatted = [{
        "region": data["region"],
        "mean_consommation": data["mean_consommation"]
    } for data in mean_cons]

    mean_cons_dict = {
        d['region']: d['mean_consommation']
        for d in mean_cons_formatted
    }

    return mean_cons_dict
