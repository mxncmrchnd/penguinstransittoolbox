# Penguin's Transit Toolbox

[![Python Version](https://img.shields.io/badge/python-%3E%3D3.9-blue.svg)]()
[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](https://unlicense.org/)
![Status](https://img.shields.io/badge/status-work--in--progress-orange)

---

**Penguin's Transit Toolbox** :  a simple python toolbox for managing GTFS data. Work in progress

---

## Summary

- [Features](#features)
- [Installation](#installation)
- [Requirements](#requirements)
- [License](#license)
- [Project Status](#project-status)
- [References](#references)

---

## Features

- Loading of GTFS files, either individually or in a dictionnary ;
- Support of both standard and spatial tables ;
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
