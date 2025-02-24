import requests
import json
from pyproj import Transformer

def wfs_query(url, polygon_coords=None, CRS="EPSG:3857", download=False):
    """
    Obtiene datos geoespaciales de todas las capas disponibles en un servicio WFS de IGAC.
    Si no se proporcionan coordenadas, obtiene todos los datos disponibles con where=1=1.

    Parámetros:
        url (str): URL del servicio WFS.
        polygon_coords (list, opcional): Lista de coordenadas del polígono en formato [[lon, lat], [lon, lat], ...].
        CRS (str, opcional): Código EPSG del sistema de referencia de coordenadas. Por defecto "EPSG:3857".
        download (bool, opcional): Indica si se debe guardar el resultado como archivo GeoJSON. Por defecto False.

    Retorna:
        list o str: Lista de características geoespaciales si `download` es False.
                    Mensaje de confirmación si `download` es True.
    """


    if polygon_coords and CRS not in ["EPSG:3857", "EPSG:102100"]:
        transformer = Transformer.from_crs(CRS, "EPSG:3857", always_xy=True)
        polygon_coords = [transformer.transform(lon, lat) for lon, lat in polygon_coords]

    response = requests.get(f"{url}?f=json")
    if response.status_code != 200:
        print("Error al obtener información del servicio:", response.status_code)
        return None

    servicio_info = response.json()
    capas_disponibles = [capa["id"] for capa in servicio_info.get("layers", [])]

    if not capas_disponibles:
        return "No se encontraron capas disponibles en el servicio."

    datos_dict = {}

    polygon_geometry = None
    if polygon_coords:
        polygon_geometry = {
            "rings": [polygon_coords],
            "spatialReference": {"wkid": 102100, "latestWkid": 3857}
        }

    for capa in capas_disponibles:
        capa_url = f"{url}/{capa}/query"

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

        response = requests.get(capa_url, params=params)
        if response.status_code == 200:
            datos_dict[f"capa_{capa}"] = response.json()
        else:
            print(f"Error al obtener datos de la capa {capa}: {response.status_code}")
            datos_dict[f"capa_{capa}"] = {}

    features = [datos_dict[capa]["features"] for capa in datos_dict if "features" in datos_dict[capa] and datos_dict[capa]["features"]]

    if download:
        geojson = {
            "features": [feature for lista in features for feature in lista]
        }
        with open("datos_WFS.geojson", "w", encoding="utf-8") as f:
            json.dump(geojson, f, indent=4, ensure_ascii=False)
        return "Archivo GeoJSON guardado como 'datos_WFS.geojson'"

    return features

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