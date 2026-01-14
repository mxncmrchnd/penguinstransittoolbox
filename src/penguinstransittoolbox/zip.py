"""
`zip` module :

SOON TO BE REMOVED
A module to read GTFS data from a ZIP file.

Notes
-----
All GTFS loader functions in this package may raise the following exceptions:

- `FileNotFoundError`: If the requested GTFS file is missing from the archive.
- `requests.exceptions.RequestException`: If downloading a remote ZIP file fails.
- `zipfile.BadZipFile`: If the file is not a valid ZIP archive.
- `ValueError`: If expected columns are missing or malformed.

These exceptions originate from internal helper functions shared by all loaders.
"""

import io
import requests
import zipfile
import pandas as pd
import geopandas as gpd
import warnings
from shapely.geometry import Point, LineString
from shapely.geometry.base import BaseGeometry
from typing import Dict, Union, Callable, Final

def _open_file(path: str, filename: str) -> pd.DataFrame:
    """
    Private function to open files from the feed.
    """
    if path.startswith(("http://", "https://")):
        response = requests.get(path)
        response.raise_for_status()
        zip_bytes = io.BytesIO(response.content)
    else:
        zip_bytes = open(path, "rb")

    with zipfile.ZipFile(zip_bytes, "r") as z:
        if filename not in z.namelist():
            raise FileNotFoundError(f"{filename} not found inside the GTFS archive.")
        with z.open(filename) as f:
            df = pd.read_csv(f)
    return df

def _validate_geometries(gdf: gpd.GeoDataFrame, name: str) -> None:
    """
    Private Function to validate geometries.
    """
    if "geometry" not in gdf.columns:
        warnings.warn(f"[{name}] has no 'geometry' column.")
        return
    geom_col = gdf["geometry"]
    missing = geom_col.isna().sum()
    if missing > 0:
        warnings.warn(f"[{name}] has {missing} missing geometries.")
    invalid = ~geom_col.apply(lambda g: isinstance(g, BaseGeometry))
    if invalid.any():
        warnings.warn(f"[{name}] has {invalid.sum()} invalid geometries (non-Shapely).")
    invalid_geom = geom_col.apply(lambda g: hasattr(g, "is_valid") and not g.is_valid)
    if invalid_geom.any():
        warnings.warn(f"[{name}] has {invalid_geom.sum()} invalid geometries (self-intersecting or corrupted).")

def read_agency(path: str) -> pd.DataFrame:
    """
    Loads the `agency.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL ;
    
    Returns
    -------
        A DataFrame containing the agency data.
    """
    return _open_file(path, "agency.txt")

def read_area(path: str) -> pd.DataFrame:
    """
    Loads the `area.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL ;
    
    Returns
    -------
        A DataFrame containing the area data.
    """
    return _open_file(path, "area.txt")

def read_attributions(path: str) -> pd.DataFrame:
    """
    Loads the `attributions.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL ;
    
    Returns
    -------
        A DataFrame containing the attributions data.
    """
    return _open_file(path, "attributions.txt")

def read_booking_rules(path: str) -> pd.DataFrame:
    """
    Loads the `booking_rules.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL ;
    
    Returns
    -------
        A DataFrame containing the booking rules data.
    """
    return _open_file(path, "booking rules.txt")

def read_calendar(path: str) -> pd.DataFrame:
    """
    Loads the `calendar.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL.
    
    Returns
    -------
        A DataFrame containing the the calendar data.
    """
    return _open_file(path, "calendar.txt")

def read_calendar_dates(path: str) -> pd.DataFrame:
    """
    Loads the `calendar_dates.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL.
    
    Returns
    -------
        A DataFrame containing the the calendar dates data.
    """
    return _open_file(path, "calendar_dates.txt")

def read_fare_attributes(path: str) -> pd.DataFrame:
    """
    Loads the `fare_attributes.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL.
    
    Returns
    -------
        A DataFrame containing the the fare attributes data.
    """
    return _open_file(path, "fare_attributes.txt")

def read_fare_leg_rules(path: str) -> pd.DataFrame:
    """
    Loads the `fare_leg_rules.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL ;
    
    Returns
    -------
        A DataFrame containing the fare leg rules data.
    """
    return _open_file(path, "fare_leg_rules.txt")

def read_fare_leg_join_rules(path: str) -> pd.DataFrame:
    """
    Loads the `fare_leg_join_rules.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL ;
    
    Returns
    -------
        A DataFrame containing the fare leg join rules data.
    """
    return _open_file(path, "fare_leg_join_rules.txt")

def read_fare_media(path: str) -> pd.DataFrame:
    """
    Loads the `fare_media.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL ;
    
    Returns
    -------
        A DataFrame containing the fare media data.
    """
    return _open_file(path,"fare_media.txt")

def read_fare_products(path: str) -> pd.DataFrame :
    """
    Loads the `fare_products.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL ;
    
    Returns
    -------
        A DataFrame containing the fare products data.
    """
    return _open_file(path, "fare_products.txt")

def read_fare_rules(path: str) -> pd.DataFrame:
    """
    Loads the `fare_rules.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL.
    
    Returns
    -------
        A DataFrame containing the the fare rules data.
    """
    return _open_file(path, "fare_rules.txt")

def read_fare_transfer_rules(path:str) -> pd.DataFrame:
    """
    Loads the `fare_transfer_rules.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL ;
    
    Returns
    -------
        A DataFrame containing the fare transfer rules data.
    """
    return _open_file(path, "fare_transfer_fules.txt")

def read_feed_info(path: str) -> pd.DataFrame:
    """
    Loads the `feed_info.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL.
    
    Returns
    -------
        A DataFrame containing the the feed info data.
    """
    return _open_file(path, "feed_info.txt")

def read_frequencies(path: str) -> pd.DataFrame:
    """
    Loads the `frequencies.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL.
    
    Returns
    -------
        A DataFrame containing the the frequencies data.
    """
    return _open_file(path, "frequencies.txt")

def read_levels(path: str) -> pd.DataFrame:
    """
    Loads the `levels.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL ;
    
    Returns
    -------
        A DataFrame containing the levels data.
    """
    return _open_file(path, "levels.txt")

def read_location_stop_groups(path: str) -> pd.DataFrame:
    """
    Loads the `location_stop_groups.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL ;
    
    Returns
    -------
        A DataFrame containing the location stop groups data.
    """
    return _open_file(path, "location_stop_groups.txt")

def read_location_groups(path: str) -> pd.DataFrame:
    """
    Loads the `location_groups.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL ;
    
    Returns
    -------
        A DataFrame containing the location groups data.
    """
    return _open_file(path, "location_groups.txt")

def read_locations(path: str) -> gpd.GeoDataFrame:
    """
    Loads the `locations.geojson` from a GTFS ZIP file (local or remote) into a GeoDataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL ;
    
    Returns
    -------
        A GeoDataFrame containing the locations data.
    
    Raises
    ------
    FileNotFoundError
        If the file is not found in the archive.
    ValueError
        If the geometry is not a Polygon or MultiPolygon.
    """
    expected_geom_types={"Polygon", "MultiPolygon"}
    if path.startswith(("http://", "https://")):
        response = requests.get(path)
        response.raise_for_status()
        zip_bytes = io.BytesIO(response.content)
    else:
        zip_bytes = open(path, "rb")
    with zipfile.ZipFile(zip_bytes, "r") as z:
        if "locations.geojson" not in z.namelist():
            raise FileNotFoundError(f"{"locations.geojson"} not found inside the GTFS archive.")       
        with z.open("locations.geojson") as f:
            gdf = gpd.read_file(f)
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")
    if isinstance(expected_geom_types, str):
        expected_geom_types = {expected_geom_types}
    actual_types = {geom.geom_type for geom in gdf.geometry if geom is not None}
    if not actual_types.issubset(expected_geom_types):
        raise ValueError(f"Geometry type mismatch: "f"expected {expected_geom_types}, found {actual_types}")
    return gdf

def read_networks(path: str) -> pd.DataFrame:
    """
    Loads the `networks.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL ;
    
    Returns
    -------
        A DataFrame containing the networks data.
    """
    return _open_file(path, "networks.txt")

def read_pathways(path: str) -> pd.DataFrame:
    """
    Loads the `pathways.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL ;
    
    Returns
    -------
        A DataFrame containing the pathways data.
    """
    return _open_file(path, "pathways.txt")

def read_rider_categories(path: str) -> pd.DataFrame:
    """
    Loads the `rider_categories.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL ;
    
    Returns
    -------
        A DataFrame containing the rider categories data.
    """
    return _open_file(path, "rider_categories.txt")

def read_route_networks(path: str) -> pd.DataFrame:
    """
    Loads the `route_networks.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL ;
    
    Returns
    -------
        A DataFrame containing the agency data.
    """
    return _open_file(path, "route_networks.txt")

def read_routes(path: str) -> pd.DataFrame:
    """
    Loads the `routes.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL.
    
    Returns
    -------
        A DataFrame containing the the routes data.
    """
    return _open_file(path, "routes.txt")

def read_shapes(path: str) -> gpd.GeoDataFrame:
    """
    Loads the `shapes.txt` from a GTFS ZIP file (local or remote) into a GeoDataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL.
    
    Returns
    -------
    shapes_gdf : GeoDataFrame
        A GeoDataFrame containing the the data, with the geometry as linestrings, in EPSG:4326.
    
    Raises
    ------
    ValueError
        If the file does not contain the required fields to create the geometry.
    """
    # Opens the file
    shapes_df = _open_file(path, "shapes.txt")
    # Checks for the required columns
    required = {"shape_id", "shape_pt_lat", "shape_pt_lon", "shape_pt_sequence"}
    if not required.issubset(shapes_df.columns):
        raise ValueError(f"shapes.txt missing columns: {required - set(shapes_df.columns)}")
    shapes_df = shapes_df.sort_values(["shape_id", "shape_pt_sequence"])
    # Creates the linestrings
    lines = (
        shapes_df.groupby("shape_id")[["shape_pt_lon", "shape_pt_lat"]]
        .apply(lambda pts: LineString(pts.to_numpy()))
        .reset_index(name="geometry")
    )
    # Creates the GeoDataFrame
    shapes_gdf = gpd.GeoDataFrame(lines, geometry="geometry", crs="EPSG:4326")
    return shapes_gdf

def read_stops(path: str) -> gpd.GeoDataFrame:
    """
    Loads the `stops.txt` from a GTFS ZIP file (local or remote) into a GeoDataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL.
    
    Returns
    -------
    stops_gdf : geopandas.GeoDataFrame
        A GeoDataFrame containing the the data, with the geometry as points, in EPSG:4326.
    
    Raises
    ------
    ValueError
        If the file does not contain the required fields to create the geometry.
    """
    # Opens the file
    stops_df = _open_file(path, "stops.txt")
    # Checks for the necessary columns
    if not {'stop_lat', 'stop_lon'}.issubset(stops_df.columns):
        raise ValueError("No latitude/longitude has been found")
    # Creates the geometry
    geometry = [Point(xy) for xy in zip(stops_df['stop_lon'], stops_df['stop_lat'])]
    # Creates the GeoDataFrame
    stops_gdf = gpd.GeoDataFrame(stops_df, geometry = geometry, crs="EPSG:4326")
    return stops_gdf

def read_stop_areas(path:str) -> pd.DataFrame:
    """
    Loads the `stop_areas.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL ;
    
    Returns
    -------
        A DataFrame containing the stop areas data.
    """
    return _open_file(path, "stop_areas.txt")

def read_stop_times(path: str) -> pd.DataFrame:
    """
    Loads the `stop_times.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL.
    
    Returns
    -------
        A DataFrame containing the the stop times data.
    """
    return _open_file(path, "stop_times.txt")

def read_timeframes(path: str) -> pd.DataFrame:
    """
    Loads the `timeframes.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL ;
    
    Returns
    -------
        A DataFrame containing the time frames data.
    """
    return _open_file(str, "timeframes.txt")

def read_transfers(path: str) -> pd.DataFrame:
    """
    Loads the `transfers.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL.
    
    Returns
    -------
        A DataFrame containing the the transfers data.
    """
    return _open_file(path, "transfers.txt")

def read_translations(path:str) -> pd.DataFrame:
    """
    Loads the `translations.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL ;
    
    Returns
    -------
        A DataFrame containing the translations data.
    """
    return _open_file(path, "translations.txt")

def read_trips(path: str) -> pd.DataFrame:
    """
    Loads the `trips.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL.
    
    Returns
    -------
        A DataFrame containing the the trips data.
    """
    return _open_file(path, "trips.txt")

def load_feed(path: str) -> Dict[str, Union[pd.DataFrame, gpd.GeoDataFrame]]:
    """
    Loads the entire GTFS feed into a dictionnary, while checking for requirements

    Required files : 
        - `agency.txt` ;
        - either `calendar.txt` or `calendar_dates.txt`
        - `routes.txt` ;
        - `trips.txt` ;
        - `stop_times.txt` ;
        - `stops.txt` unless `locations.geojson` is provided, in which case stops are optional.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL.

    Returns
    -------
    Dict[str, Union[pandas.DataFrame, geopandas.GeoDataFrame]]
        A dictionnary containing the GTFS feed data

    Raises
    ------
    FileNotFoundError
        If any required file is missing.
    Exception
        If any exception in the loaders occured (unless caught and skipped).
    """
    # Lists all loaders
    current_module = globals()
    loaders: Dict[str, Callable]={
        name[5:]: func
        for name, func in current_module.items()
        if callable(func) and name.startswith("read_")
    }
    # Required files
    REQUIRED = {"agency", "routes", "trips", "stop_times"}
    CALENDAR_ALTERNATIVE={"calendar", "calendar_dates"}
    # Lists available file
    if path.startswith(("http://", "https://")):
        response = requests.get(path)
        response.raise_for_status()
        zip_bytes = io.BytesIO(response.content)
    else:
        zip_bytes = open(path, "rb")

    with zipfile.ZipFile(zip_bytes, "r") as z:
        available_files = set(z.namelist())
    available_names = {
        fname.replace(".txt", "")
        for fname in available_files
        if fname.endswith(".txt")
    }
    available_geojson = {
        fname.replace(".geojson", "")
        for fname in available_files
        if fname.endswith(".geojson")
    }
    # Handling stops.txt/locations.geojson
    has_locations = "locations" in available_geojson
    has_stops = "stops" in available_names
    if not has_locations and not has_stops:
        raise FileNotFoundError(
            "GTFS feed must include either stops.txt or locations.geojson. "
            "Neither was found."
        )
    if has_stops:
        REQUIRED = REQUIRED | {"stops"}
    # Checks required files and calendars
    missing_required = REQUIRED - available_names
    if missing_required:
        raise FileNotFoundError(
            "Required GTFS file(s) missing: " +
            ", ".join(f"{name}.txt" for name in sorted(missing_required))
        )
    if not (CALENDAR_ALTERNATIVE & available_names):
        raise FileNotFoundError(
            "GTFS feed must include at least one of: "
            "calendar.txt or calendar_dates.txt"
        )
    # Loads files
    feed: Dict[str, Union[pd.DataFrame, gpd.GeoDataFrame]] = {}
    for name, func in loaders.items():
        txt_name = f"{name}.txt"
        geojson_name = f"{name}.geojson"

        if txt_name in available_files or geojson_name in available_files:
            try:
                feed[name] = func(path)

                # Validate geometries for GeoDataFrames
                if isinstance(feed[name], gpd.GeoDataFrame):
                    _validate_geometries(feed[name], name)

            except Exception as e:
                print(f"Skipping {name}: {e}")
    return feed