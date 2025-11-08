# Penguin's Transit Toolbox

[![Python Version](https://img.shields.io/badge/python-%3E%3D3.9-blue.svg)]()
[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](https://unlicense.org/)
![Status](https://img.shields.io/badge/status-work--in--progress-orange)
[![Documentation](https://img.shields.io/badge/docs-online-blue)](https://mxncmrchnd.github.io/penguinstransittoolbox/penguinstransittoolbox.html)

---

**Penguin's Transit Toolbox** :  a simple python toolbox for managing GTFS data. Work in progress

---

## Summary

- [Features](#features)
- [Installation](#installation)
- [Usage examples](#usage-examples)
- [Documentation](#documentation)
- [Requirements](#requirements)
- [License](#license)
- [Project Status](#project-status)
- [References](#references)

---

## Features

- Loading of GTFS files, either individually or in a dictionnary ;
- Support of both standard and spatial tables ;
- Export of `stops` and `shapes` as GIS-ready files ;
- Detection of available files ;
- Geometry validation ;
- Compatibility with `pandas`, `geopandas` and `shapely`.

---

## Installation

For local development only (for now).
```bash
pip install -e .
```

---

## Usage examples

Importing the package :
```python
import penguinstransittoolbox as ptt
```

Loading a feed and exporting its geographical features to GIS-ready files :
```python
feed = ptt.zip.load_feed('example/feed.zip')
# export the stops as GeoPackage (the default output format)
ptt.gis.export_stops(feed['stops'], output='stops.gpkg')
# export the shapes as ESRI Shapefile
ptt.gis.export_shapes(feed['shapes'], output='shapes.shp', format='Shapefile')
```

## Documentation

The documentation is available [here](https://img.shields.io/badge/docs-online-blue)](https://mxncmrchnd.github.io/penguinstransittoolbox/penguinstransittoolbox.html).

## Requirements

- Python >= 3.9
- pandas >= 1.5
- geopandas >= 0.13
- shapely >= 2.0
- requests >= 2.30

---

## License

This project is released under **The Unlicense**, dedicated to the public domain.

---

## Project Status

This project is in early development and subject to change.
Contributions, feedback and issue reports are welcome.

## References

- [GTFS specification](https://gtfs.org/fr/)
- [pandas](https://pandas.pydata.org/)
- [geopandas](https://geopandas.org/en/stable/)
- [shapely](https://shapely.readthedocs.io/en/stable/manual.html)
- [requests](https://requests.readthedocs.io/en/latest/)
