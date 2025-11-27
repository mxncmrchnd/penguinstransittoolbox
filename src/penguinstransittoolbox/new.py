"""
`new` module : 

A module to create an empty feed.
"""

import pandas as pd
import geopandas as gpd

def agency() -> pd.DataFrame :
    """
    Creates an empty `DataFrame` with the required columns for the `agency`.
    
    Returns
    -------
    agency_gdf : DataFrame
        An empty DataFrame with the following columns :

        - `agency_id` : the unique ID of the agency ;
        - `agency_name` : the name of the agency ;
        - `agency_url` : the URL of the agency's website ;
        - `agency_timezone` : the timezone of the agency ;
        - `agency_lang` : the language of the agency ;
        - `agency_phone` : the phone number of the agency ;
        - `agency_fare_url` : the URL of the agency's online store ;
        - `agency_email` : the email adress of the agency ;
        - `cemv_support` : whether the agency supports CEMV or not.

    Note
    ----
    All columns are of `object` dtype.
    """
    agency_df = pd.DataFrame({
        'agency_id': pd.Series(dtype='int64'),
        'agency_name': pd.Series(dtype='str'),
        'agency_url': pd.Series(dtype='str'),
        'agency_timezone': pd.Series(dtype='str'),
        'agency_lang': pd.Series(dtype='str'),
        'agency_phone': pd.Series(dtype='str'),
        'agency_fare_url': pd.Series(dtype='str'),
        'agency_email': pd.Series(dtype='str'),
        'cemv_support': pd.Series(dtype='uint8')
    })
    return agency_df