import geopandas as gpd
from shapely import Point
from typing import Literal


"""
Internal function to check if the geodataframe is a correct `stops` file (contains stop_id, stop_name and coordinates) as well as a Point geometry
"""
def _validate_stops(stops_gdf: gpd.GeoDataFrame) -> None:
    cols = {"stop_id", "stop_name", "stop_lat", "stop_lon"}
    if not cols.issubset(stops_gdf.columns):
        raise ValueError(f"The GeoDataFrame is not a correct stops files, missing : {cols - set(stops_gdf.columns)}")
    if stops_gdf.geometry.is_empty.all():
        raise ValueError("The GeoDataFrame has no valid geometries.")
    
def export_stops(stops_gdf: gpd.GeoDataFrame, output: str, format: Literal["GeoPackage", "GeoJSON", "Shapefile"]="GeoPackage") -> None:
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
    stops_gdf.to_file(output, driver=driver)
    print(f"Stops correctly exported to {output}")