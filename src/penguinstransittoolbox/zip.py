"""
`zip` module
============

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
from typing import Dict, Union, Callable

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
        The path to the source ZIP file. Can be a local path or an URL.
    
    Returns
    -------
        A GeoDataFrame containing the the agency data.
    """
    return _open_file(path, "agency.txt")

def read_calendar(path: str) -> pd.DataFrame:
    """
    Loads the `calendar.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL.
    
    Returns
    -------
        A GeoDataFrame containing the the calendar data.
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
        A GeoDataFrame containing the the calendar dates data.
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
        A GeoDataFrame containing the the fare attributes data.
    """
    return _open_file(path, "fare_attributes.txt")

def read_fare_rules(path: str) -> pd.DataFrame:
    """
    Loads the `fare_rules.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL.
    
    Returns
    -------
        A GeoDataFrame containing the the fare rules data.
    """
    return _open_file(path, "fare_rules.txt")

def read_feed_info(path: str) -> pd.DataFrame:
    """
    Loads the `feed_info.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL.
    
    Returns
    -------
        A GeoDataFrame containing the the feed info data.
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
        A GeoDataFrame containing the the frequencies data.
    """
    return _open_file(path, "frequencies.txt")

def read_routes(path: str) -> pd.DataFrame:
    """
    Loads the `routes.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL.
    
    Returns
    -------
        A GeoDataFrame containing the the routes data.
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

def read_stop_times(path: str) -> pd.DataFrame:
    """
    Loads the `stop_times.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL.
    
    Returns
    -------
        A GeoDataFrame containing the the stop times data.
    """
    return _open_file(path, "stop_times.txt")

def read_transfers(path: str) -> pd.DataFrame:
    """
    Loads the `transfers.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL.
    
    Returns
    -------
        A GeoDataFrame containing the the transfers data.
    """
    return _open_file(path, "transfers.txt")

def read_trips(path: str) -> pd.DataFrame:
    """
    Loads the `trips.txt` from a GTFS ZIP file (local or remote) into a DataFrame.

    Parameters
    ----------
    path : str
        The path to the source ZIP file. Can be a local path or an URL.
    
    Returns
    -------
        A GeoDataFrame containing the the trips data.
    """
    return _open_file(path, "trips.txt")

def load_feed(path: str) -> Dict[str, Union[pd.DataFrame, gpd.GeoDataFrame]]:
    """
    Loads an entire GTFS feed (ZIP file or URL) into memory.

    This master loader automatically detects and calls all `read_*` functions 
    defined in this module. Each `read_*` function loads a specific GTFS 
    component (e.g., stops, routes, trips) and returns a DataFrame or 
    GeoDataFrame as appropriate.

    Parameters
    ----------
    path : str
        Path or URL to the GTFS ZIP file. Both local and remote files are supported.

    Returns
    -------
    feed : dict of {str: pandas.DataFrame or geopandas.GeoDataFrame}
        A dictionary mapping GTFS component names (without `.txt`) to their 
        corresponding DataFrames or GeoDataFrames.  
        For example:
        
        {
            "agency": DataFrame,
            "stops": GeoDataFrame,
            "routes": DataFrame,
            "trips": DataFrame,
            "stop_times": DataFrame,
            "calendar": DataFrame,
            "calendar_dates": DataFrame,
            "shapes": GeoDataFrame,
            ...
        }

    Notes
    -----
    - The loader automatically discovers all functions named `read_*` in this module.
    - Only GTFS files present in the ZIP archive are loaded; missing optional files
      are skipped silently (with a warning).
    - `stops` and `shapes` are typically returned as GeoDataFrames; all others 
      are standard pandas DataFrames.
    - Geometry validation is performed automatically for all GeoDataFrames.

    Raises
    ------
    - requests.exceptions.RequestException
        If downloading a remote GTFS feed fails.
    
    - zipfile.BadZipFile
        If the provided file is not a valid ZIP archive.
    
    - ValueError
        If a loader encounters invalid or corrupted data.
    """
    # Gets the list of functions
    current_module = globals()
    loaders : Dict[str, Callable]={
        name[5:]: func
        for name, func in current_module.items()
        if callable(func) and name.startswith("read_")
    }
    # Checks the files availability
    if path.startswith(("http://", "https://")):
        response = requests.get(path)
        response.raise_for_status()
        zip_bytes = io.BytesIO(response.content)
    else:
        zip_bytes = open(path, "rb")
    with zipfile.ZipFile(zip_bytes, "r") as z:
        available_files = set(z.namelist())
    # Creates the dictionnary
    feed: Dict[str, Union[pd.DataFrame, gpd.GeoDataFrame]] = {}
    # Fills the dictionnary by calling each loader
    for name, func in loaders.items():
        fname = f"{name}.txt"
        if fname in available_files:
            try:
                feed[name] = func(path)
                # Validates the geometry for the spatial tables (stops and shapes)
                if isinstance(feed[name], gpd.GeoDataFrame):
                    _validate_geometries(feed[name], name)
            except Exception as e:
                print(f"Skipping {fname}: {e}")
    return feed