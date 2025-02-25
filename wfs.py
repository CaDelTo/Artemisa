import requests
import json
from pyproj import Transformer

def wfs_query(url, polygon_coords=None, CRS="EPSG:3857", download=False):
    """
    Gets geospatial data from all available layers in an IGAC WFS service.
    If no coordinates are provided, gets all available data.

    Parameters:
        url (str): WFS service URL.
        polygon_coords (list, optional): List of polygon coordinates in format [[lon, lat], [lon, lat], ...].
        CRS (str, optional): EPSG code of the coordinate reference system. Default "EPSG:3857".
        download (bool, optional): Indicates if result should be saved as GeoJSON file. Default False.

    Returns:
        list or str: List of geospatial features if `download` is False.
                     Confirmation message if `download` is True.
    """

    if polygon_coords and CRS not in ["EPSG:3857", "EPSG:102100"]:
        transformer = Transformer.from_crs(CRS, "EPSG:3857", always_xy=True)
        polygon_coords = [transformer.transform(lon, lat) for lon, lat in polygon_coords]

    response = requests.get(f"{url}?f=json")
    if response.status_code != 200:
        return f"Error getting service information: {response.status_code}"

    service_info = response.json()
    available_layers = [layer["id"] for layer in service_info.get("layers", [])]

    if not available_layers:
        return "No layers found in the service."

    data_dict = {}

    polygon_geometry = None
    if polygon_coords:
        polygon_geometry = {
            "rings": [polygon_coords],
            "spatialReference": {"wkid": 102100, "latestWkid": 3857}
        }

    for layer in available_layers:
        layer_url = f"{url}/{layer}/query"

        params = {
            "f": "json",
            "returnGeometry": "true",
            "outFields": "*",
        }

        if polygon_geometry:
            params["spatialRel"] = "esriSpatialRelIntersects"
            params["geometry"] = json.dumps(polygon_geometry)
            params["geometryType"] = "esriGeometryPolygon"
        else:
            params["where"] = "1=1"

        response = requests.get(layer_url, params=params)
        if response.status_code == 200:
            data_dict[f"layer_{layer}"] = response.json()
        else:
            print(f"Error getting data from layer {layer}: {response.status_code}")
            data_dict[f"layer_{layer}"] = {}

    features = [data_dict[layer]["features"] for layer in data_dict if "features" in data_dict[layer] and data_dict[layer]["features"]]

    if download:
        geojson = {
            "features": [feature for sublist in features for feature in sublist]
        }
        with open("WFS_data.geojson", "w", encoding="utf-8") as f:
            json.dump(geojson, f, indent=4, ensure_ascii=False)
        return "GeoJSON file saved as 'WFS_data.geojson'"

    return features

#Ej de uso
url_igac = "https://mapas2.igac.gov.co/server/rest/services/geodesia/redgravimetrica/MapServer"
polygon_coords = [
    [-74.12, 4.65],  # Punto 1
    [-74.16, 4.68],  # Punto 2
    [-74.10, 4.70],  # Punto 3
    [-74.05, 4.68],  # Punto 4
    [-74.06, 4.64],  # Punto 5
    [-74.10, 4.62],  # Punto 6
    [-74.15, 4.63]
]


datos = wfs_query(url_igac,polygon_coords , CRS="EPSG:4326", download=False)
print(datos)