"""
Penguin's Transit Toolbox
=========================

A python package to manage GTFS feeds.
Compatible with the GTFS Fares-v2 extension proposal.
Development is currently paused.

Modules
-------


"""

from importlib import import_module

__all__ = [

]

def __getattr__(name):
    if name in __all__:
        return import_module(f".{name}", __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
