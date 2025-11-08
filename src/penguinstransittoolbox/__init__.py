"""
Penguin's Transit Toolbox
=========================

A python package to manage GTFS feeds.

Modules
-------
zip : 
    A module to read GTFS data from a ZIP file.

gis :
    A module to export stops and shapes as GIS-ready files.

"""

from importlib import import_module

__all__ = [
    "zip",
    "gis"
]

def __getattr__(name):
    if name in __all__:
        return import_module(f".{name}", __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")