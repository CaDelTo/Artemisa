# Original Base Service Scripts & Web Scraping

This directory contains the original Python scripts used for extracting geospatial data from various services (ArcGIS, WMS, WFS) and a web scraping script. These scripts were used at the beginning of the project to obtain the necessary service URLs.

## Structure

- `arcgis.py` - Extracts data from ArcGIS services.
- `wms.py` - Extracts data from Web Map Service (WMS).
- `wfs.py` - Extracts data from Web Feature Service (WFS).
- `web_scrap.py` - Web scraper to collect links to geospatial services.

## Usage

Each script can be executed independently. They require Python 3 and some dependencies (e.g., `requests`, `BeautifulSoup`) that need to be installed beforehand.
