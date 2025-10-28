"""
Penguin's Transit Toolbox
=========================

A lightweight GTFS (General Transit Feed Specification) loader package
for reading and managing transit feed data directly from ZIP archives
or URLs.

This package provides a collection of loader functions that read
individual GTFS components (stops, routes, trips, etc.) and a master
loader that aggregates all available files in a feed.

Modules
-------
gtfs_loader : 
    Contains all `zip_*` loader functions, the shared helper functions, 
    and the `load_gtfs_feed()` master loader.

Usage
-----
>>> from gtfs_tools import load_gtfs_feed
>>> feed = load_gtfs_feed("https://transitfeeds.com/p/mbta/64/latest/download")
>>> feed["stops"].head()

"""

from .zip_utils import (
    zip_agency,
    zip_calendar,
    zip_calendar_dates,
    zip_fare_attributes,
    zip_fare_rules,
    zip_feed_info,
    zip_frequencies,
    zip_routes,
    zip_shapes,
    zip_stop_times,
    zip_stops,
    zip_transfers,
    zip_trips,
    load_feed
)

__all__ = [
    "zip_agency",
    "zip_calendar",
    "zip_calendar_dates",
    "zip_fare_attributes",
    "zip_fare_rules",
    "zip_feed_info",
    "zip_frequencies",
    "zip_routes",
    "zip_shapes",
    "zip_stop_times",
    "zip_stops",
    "zip_transfers",
    "zip_trips",
    "load_feed"
]