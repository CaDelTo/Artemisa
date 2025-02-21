import requests
import json
import geopandas as gpd
from shapely.geometry import shape
from pyproj import Transformer

def arcgis_query(url, lat_min, lon_min, lat_max, lon_max, CRS = "EPSG:4326", download=False):
    """
    Obtiene datos geoespaciales de todas las capas disponibles en un servicio ArcGIS de Catastro Bogotá
    dentro de un área definida por un Bounding Box (BBox) en coordenadas WGS 84.

    Parámetros:
        url (str): URL base del servicio ArcGIS.
        lat_min (float): Latitud mínima (esquina inferior izquierda).
        lon_min (float): Longitud mínima (esquina inferior izquierda).
        lat_max (float): Latitud máxima (esquina superior derecha).
        lon_max (float): Longitud máxima (esquina superior derecha).
        CRS (str, opcional): Código EPSG del sistema de referencia de coordenadas.
            Por defecto "EPSG:3857".
        download (bool, opcional): Indica si se debe guardar el resultado como archivo GeoJSON.
            Por defecto False.

    Retorna:
        dict o str: Diccionario con los datos geoespaciales si `download` es False.
                    Mensaje de confirmación si `download` es True.
    """


    if CRS not in ["EPSG:4326"]:
        transformer = Transformer.from_crs(CRS, "EPSG:4326", always_xy=True)
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

    polygon_geometry = {
        "rings": [[
            [lon_min, lat_min],
            [lon_min, lat_max],
            [lon_max, lat_max],
            [lon_max, lat_min],
            [lon_min, lat_min]
        ]],
        "spatialReference": {"wkid": 4326}
    }

    for capa in capas_disponibles:
        capa_url = f"{url}/{capa}/query"
        params = {
            "where": "1=1",  # Consulta todos los datos
            "outFields": "*",
            "f": "geojson",  # Formato GeoJSON
            "returnGeometry": "true",
            "geometry": json.dumps(polygon_geometry),
            "geometryType": "esriGeometryPolygon",
            "spatialRel": "esriSpatialRelIntersects",
            "inSR": 4326,  # Sistema de referencia espacial
            "geometryPrecision": 5
        }

        response = requests.get(capa_url, params=params)
        if response.status_code == 200:
            geojson_data = response.json()
            if "features" in geojson_data and geojson_data["features"]:
                datos_dict = geojson_data["features"]
            else:
                datos_dict = []
        else:
            print(f"Error al obtener datos de la capa {capa}: {response.status_code}")
            datos_dict[f"capa_{capa}"] = []

    if download:
        with open("datos_ArcGis.geojson", "w", encoding="utf-8") as f:
            json.dump(datos_dict, f, indent=4, ensure_ascii=False)
        return "Archivo GeoJSON guardado como 'datos.geojson'"

    return datos_dict

# Ejemplo de uso
url_catastro = "https://mapas.igac.gov.co/server/rest/services/centrocontrol/EstacionesGNSS/MapServer"
lat_min, lon_min, lat_max, lon_max = 2.73372, -73.99826, 7.72174, -76.04641
datos = arcgis_query(url_catastro, lat_min, lon_min, lat_max, lon_max, "EPSG:4326", download=True)

print(datos)