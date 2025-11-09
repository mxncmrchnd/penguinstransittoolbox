"""
Penguin's Transit Toolbox
=========================

A python package to manage GTFS feeds.

Modules
-------
edit :
    A module to edit an existing feed.

gis :
    A module to work with `stops`and `shapes` as GIS files.

new :
    A module to create an empty feed.

zip : 
    A module to read GTFS data from a ZIP file.

"""

from importlib import import_module

__all__ = [
    "edit",
    "gis",
    "new",
    "zip"
]

def __getattr__(name):
    if name in __all__:
        return import_module(f".{name}", __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")