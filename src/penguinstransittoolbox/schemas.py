"""
GTFS table schemas definitions.

These schemas define the columns and types of each file.
"""

from typing import Dict

AGENCY_SCHEMA : Dict[str, str]={
    "agency_id" : "object",
    "agency_name" : "object",
    "agency_url" : "object",
    "agency_timezone" : "object",
    "agency_lang" : "object",
    "agency_phone" : "object",
    "agency_fare_url" : "object",
    "agency_email" : "object",
    "cemv_support" : "int8"
}
"""
Schema for the `agency` file. All fields are of `object` dtype, except `cemv_support`, which is of `int8` dtype.
"""
CALENDAR_SCHEMA : Dict[str, str]={
     "service_id" : "object",
     "monday" : "int8",
     "tuesday" : "int8",
     "wednesday" : "int8",
     "thursday" : "int8",
     "friday" : "int8",
     "saturday" : "int8",
     "sunday" : "int8",
     "start_date" : "int64",
     "end_date" : "int64"
}
"""
Schema for the `calendar` file. `service_id` is of `object` dtype. Weekdays or of `int8` dtype, to allow `NA` values in incomplete feeds. Start and end dates are of `int64` dtype, as dates are stored as YYYYMMDD format.
"""