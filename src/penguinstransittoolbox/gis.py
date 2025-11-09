import geopandas as gpd
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
    
def _validate_shapes(shapes_gdf: gpd.GeoDataFrame) -> None:
    """
    Internal function to check if the geodataframe is a correct `shapes` file.
    """
    if not isinstance(shapes_gdf, gpd.GeoDataFrame):
        raise ValueError("The table must be a GeoDataFrame.")
    if "shape_id" not in shapes_gdf.columns:
        raise ValueError("The table does not containe a `shape_id` column")
    if shapes_gdf.geometry.is_empty.all():
        raise ValueError("The GeoDataFrame has no valid geometries.")
    if not (shapes_gdf.geom_type == "LineString").all():
        raise ValueError("Some geometries in stops_gdf are not Point geometries.")
    
def export_shapes(shapes_gdf: gpd.GeoDataFrame, output: str, format: Literal["GeoPackage", "GeoJSON", "Shapefile"]="GeoPackage") -> None:
    """
    Exports a `shapes` GeoDataFrame as a vector layer (gpkg, geojson or shp).

    Parameters
    ----------
    shapes_gdf : gpd.GeoDataFrame
        The GeoDataFrame containing the shapes.
    output : str
        The output file path and name.
    format : {"GeoPackage", "GeoJSON", "Shapefile"}, default "GeoPackage"
        The output file format

    Raises
    ------
    ValueError
        If the input file is not correct (must be a GeoDataFrame, with no missing required colums, and a LineString geometry)
    OSError
        If there was an error when writing the file
        
    """
    # Checks if the provided GeoDataFrame is valid
    _validate_shapes(shapes_gdf)
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
    try :
        shapes_gdf.to_file(output, driver=driver)
        print(f"Shapes correctly exported to {output}")
    except Exception as e:
        raise OSError(f"Failed to export shapes: {e}")

def export_stops(stops_gdf: gpd.GeoDataFrame, output: str, format: Literal["GeoPackage", "GeoJSON", "Shapefile"]="GeoPackage") -> None:
    """
    Exports a `stops` GeoDataFrame as a vector layer (gpkg, geojson or shp).

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
    try :
        stops_gdf.to_file(output, driver=driver)
        print(f"Stops correctly exported to {output}")
    except Exception as e:
        raise OSError(f"Failed to export shapes: {e}")
    
def shapes_from_gis(shapes:str)->gpd.GeoDataFrame :
    """
    Reads a `shapes` GeoDataFrame from a GIS file.

    Parameters
    ----------
    shapes : str
        The GIS file containing the `stops`.

    Returns
    -------
    shapes_gdf : geopandas.GeoDataFrame
        A GeoDataFrame containing the the data, with the geometry as lines, in EPSG:4326.

    Raises
    ------
    ValueError
        If any of the following conditions is met :

        - The required field (`shape_id`) is not present.
        - The geometry is empty.
        - The geometry is not a line.
        - The CRS is not EPSG:4326.

    """
    # Loads the shapes from a GIS file
    shapes_gdf = gpd.read_file(shapes)
    # Checks for the required fields
    required_field = {"shape_id"}
    missing = required_field - set(shapes_gdf.columns)
    if missing:
      raise ValueError(f"Missing required shapes fields: {', '.join(missing)}")
    # Checks the geometry
    if shapes_gdf.geometry.is_empty.any():
      raise ValueError("Shape geometries contain empty features.")
    valid_types = {"LineString", "MultiLineString"}
    if not shapes_gdf.geometry.geom_type.isin(valid_types).all():
      raise ValueError("Shape geometries must all be of type 'LineString' or 'MultiLineString'.")
    # Checks the CRS (if there is one, and if it is EPSG:4326)
    if shapes_gdf.crs is None:
        print("Warning: No CRS defined. Assuming EPSG:4326 (WGS84).")
        shapes_gdf.set_crs("EPSG:4326", inplace=True)
    if shapes_gdf.crs.to_epsg() != 4326:
      raise ValueError(f"Invalid CRS: {shapes_gdf.crs}. Expected EPSG:4326 (WGS84).")
    # Returns the GeoDataFrame
    print("Shapes correctly imported from GIS file")
    return shapes_gdf

def stops_from_gis(stops:str)->gpd.GeoDataFrame :
    """
    Reads a `stops` GeoDataFrame from a GIS file.

    Parameters
    ----------
    stops : str
        The GIS file containing the `stops`.

    Returns
    -------
    stops_gdf : geopandas.GeoDataFrame
        A GeoDataFrame containing the the data, with the geometry as points, in EPSG:4326.

    Raises
    ------
    ValueError
        If any of the following conditions is met :

        - The required fields (`stops_id` and `stop_name`) are not present.
        - The geometry is empty.
        - The geometry is not a point.
        - The CRS is not EPSG:4326.

    """
    # Loads the stops from a GIS file
    stops_gdf = gpd.read_file(stops)
    # Checks for the required fields
    required_fields = {"stop_id", "stop_name"}
    missing = required_fields - set(stops_gdf.columns)
    if missing:
      raise ValueError(f"Missing required stop fields: {', '.join(missing)}")
    # Checks the geometry
    if stops_gdf.geometry.is_empty.any():
      raise ValueError("Stop geometries contain empty features.")
    if not stops_gdf.geometry.geom_type.isin(["Point"]).all():
      raise ValueError("Stop geometries must all be of type 'Point'.")
    # Checks the CRS (if there is one, and if it is EPSG:4326)
    if stops_gdf.crs is None:
        print("Warning: No CRS defined. Assuming EPSG:4326 (WGS84).")
        stops_gdf.set_crs("EPSG:4326", inplace=True)
    if stops_gdf.crs.to_epsg() != 4326:
      raise ValueError(f"Invalid CRS: {stops_gdf.crs}. Expected EPSG:4326 (WGS84).")
    # Returns the GeoDataFrame
    print("Stops correctly imported from GIS file")
    return stops_gdf