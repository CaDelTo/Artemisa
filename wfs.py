import requests
import json
from pyproj import Transformer

def wfs_query(url, lat_min, lon_min, lat_max, lon_max, CRS = "EPSG:3857", download=False):
    """
    Obtiene datos geoespaciales de todas las capas disponibles en un servicio WFS de IGAC
    dentro de un área definida por un Bounding Box (BBox) en coordenadas WGS 84.

    Parámetros:
        url (str): URL del servicio WFS.
        lat_min (float): Latitud mínima (esquina inferior izquierda).
        lon_min (float): Longitud mínima (esquina inferior izquierda).
        lat_max (float): Latitud máxima (esquina superior derecha).
        lon_max (float): Longitud máxima (esquina superior derecha).
        CRS (str, opcional): Código EPSG del sistema de referencia de coordenadas.
            Por defecto "EPSG:3857".
        download (bool, opcional): Indica si se debe guardar el resultado como archivo GeoJSON.
            Por defecto False.

    Retorna:
        list o str: Lista de características geoespaciales si `download` es False.
                    Mensaje de confirmación si `download` es True.
    """


    if CRS not in ["EPSG:3857", "EPSG:102100"]:
        transformer = Transformer.from_crs(CRS, "EPSG:3857", always_xy=True)
        lon_min, lat_min = transformer.transform(lon_min, lat_min)
        lon_max, lat_max = transformer.transform(lon_max, lat_max)

    response = requests.get(f"{url}?f=json")
    if response.status_code != 200:
        print("Error al obtener información del servicio:", response.status_code)
        return None

    servicio_info = response.json()
    capas_disponibles = [capa["id"] for capa in servicio_info.get("layers", [])]

    if not capas_disponibles:
        return "No se encontraron capas disponibles en el servicio."

    datos_dict = {}

    for capa in capas_disponibles:
        capa_url = f"{url}/{capa}/query"
        params = {
            "f": "json",
            "returnGeometry": "true",
            "spatialRel": "esriSpatialRelIntersects",
            "geometry": json.dumps({
                "xmin": lon_min, "ymin": lat_min, "xmax": lon_max, "ymax": lat_max,
                "spatialReference": {"wkid": 102100, "latestWkid": 3857}
            }),

            "geometryType": "esriGeometryEnvelope",
            "outFields": "*",
        }

        response = requests.get(capa_url, params=params)
        if response.status_code == 200:
            datos_dict[f"capa_{capa}"] = response.json()
        else:
            print(f"Error al obtener datos de la capa {capa}: {response.status_code}")
            datos_dict[f"capa_{capa}"] = {}

    features_solo = [datos_dict[capa]["features"] for capa in datos_dict if "features" in datos_dict[capa] and datos_dict[capa]["features"]]

    if download:
        geojson = {
            "features": [feature for lista in features_solo for feature in lista]
        }
        with open("datos_WFS.geojson", "w", encoding="utf-8") as f:
            json.dump(datos_dict, f, indent=4, ensure_ascii=False)
        return "Archivo GeoJSON guardado como 'datos.geojson'"

    return features_solo

# Ejemplo de uso
url_igac = "https://mapas2.igac.gov.co/server/rest/services/geodesia/redgravimetrica/MapServer"
lat_min, lon_min, lat_max, lon_max = 6.24, -73, 6.3, -74

datos = wfs_query(url_igac, lat_min, lon_min, lat_max, lon_max, "EPSG:4326", download=True)


