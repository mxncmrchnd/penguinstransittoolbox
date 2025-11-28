"""
`new` module : 

A module to create an empty feed.
See penguinstransittoolbox.schemas for more informations about columns and types for each file.
"""

import pandas as pd
import geopandas as gpd

from . import schemas

def agency() -> pd.DataFrame :
    """
    Creates an empty `agency` DataFrame.
    
    Returns
    -------
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

    See also
    --------
    penguinstransittoolbox.schemas.AGENCY_SCHEMA
    """
    return pd.DataFrame({
        col: pd.Series(dtype=dtype)
        for col, dtype in schemas.AGENCY_SCHEMA.items()
    })

def calendar() -> pd.DataFrame:
    """
    Creates an empty `calendar` DataFrame.

    Returns
    -------
    An empty DataFrame containing the following columns :

        - `service_id` : the service ID ;
        - `monday` : indicates if the service operates on mondays (`monday` = 1) or not (`monday` = 1) ;
        - `tuesday` : same as above, but for tuesdays ;
        - `wednesday` : same as above, but for wednesdays ;
        - `thursday` : same as above, but for thursdays ;
        - `friday` : same as above, but for fridays ;
        - `saturday` : same as above, but for saturdays ;
        - `sunday` : same as above, but for sundays ;
        - `start_date` : the start date for the service, in YYYYMMDD format ;
        - `end_date` : the end date for the service, in YYYYMMDD format.

    See also
    --------
    penguinstransittoolbox.schemas.CALENDAR_SCHEMA
    """
    return pd.DataFrame({
        col: pd.Series(dtype=dtype)
        for col, dtype in schemas.CALENDAR_SCHEMA.items()
    })