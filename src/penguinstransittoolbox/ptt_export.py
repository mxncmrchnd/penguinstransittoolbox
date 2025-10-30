import geopandas as gpd
from shapely import Point
from typing import Literal

"""
Stops and Shapes exporter from GeoDataFrames
--------------------------------------------
Functions to export stops and shapes as GIS-ready files.
"""

def _validate_stops(stops_gdf: gpd.GeoDataFrame) -> None:
    """
    Internal function to check if the geodataframe is a correct `stops` file (contains stop_id, stop_name and coordinates) as well as a Point geometry
    """
    if not isinstance(stops_gdf, gpd.GeoDataFrame):
        raise ValueError("The table must be a GeoDataFrame.")
    cols = {"stop_id", "stop_name", "stop_lat", "stop_lon"}
    if not cols.issubset(stops_gdf.columns):
        raise ValueError(f"The GeoDataFrame is not a correct stops files, missing : {cols - set(stops_gdf.columns)}")
    if stops_gdf.geometry.is_empty.all():
        raise ValueError("The GeoDataFrame has no valid geometries.")
    if not (stops_gdf.geom_type == "Point").all():
        raise ValueError("Some geometries in stops_gdf are not Point geometries.")
   
def export_stops(stops_gdf: gpd.GeoDataFrame, output: str, format: Literal["GeoPackage", "GeoJSON", "Shapefile"]="GeoPackage") -> None:
    """
    Exports a `stops` GeoDataFrame as a vetor layer (gpkg, geojson or shp).

    Parameters
    ----------
    stops_gdf : gpd.GeoDataFrame
        The GeoDataFrame containing the stops.
    output : str
        The output file path and name.
    format : {"GeoPackage", "GeoJSON", "Shapefile"}, default "GeoPackage"
        The output file format

    Raises
    ------
    ValueError
        If the input file is not correct (must be a GeoDataFrame, with no missing required colums, and a Point geometry)
    OSError
        If there was an error when writing the file
        
    """
    # Checks if the provided GeoDataFrame is valid
    _validate_stops(stops_gdf)
    # Checks if the format is a supported format
    driver_map={
        "GeoPackage": "GPKG",
        "GeoJSON": "GeoJSON",
        "Shapefile": "ESRI Shapefile"
    }
    driver = driver_map.get(format)
    if not driver:
        raise ValueError(f"Unsupported format : {format}")
    # Writes the file and prints a success message
    stops_gdf.to_file(output, driver=driver)
    print(f"Stops correctly exported to {output}")