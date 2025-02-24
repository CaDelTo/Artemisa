import requests
import json
from pyproj import Transformer

def arcgis_query(url, polygon_coords=None, CRS="EPSG:4326", download=False):
    """
    Obtiene datos geoespaciales de todas las capas disponibles en un servicio ArcGIS de Catastro Bogotá.
    Si no se proporcionan coordenadas, obtiene todos los datos disponibles con where=1=1.

    Parámetros:
        url (str): URL base del servicio ArcGIS.
        polygon_coords (list, opcional): Lista de coordenadas del polígono en formato [[lon, lat], [lon, lat], ...].
        CRS (str, opcional): Código EPSG del sistema de referencia de coordenadas. Por defecto "EPSG:4326".
        download (bool, opcional): Indica si se debe guardar el resultado como archivo GeoJSON. Por defecto False.

    Retorna:
        dict o str: Diccionario con los datos geoespaciales si `download` es False.
                    Mensaje de confirmación si `download` es True.
    """

    if polygon_coords and CRS != "EPSG:4326":
        transformer = Transformer.from_crs(CRS, "EPSG:4326", always_xy=True)
        polygon_coords = [transformer.transform(lon, lat) for lon, lat in polygon_coords]

    response = requests.get(f"{url}?f=json")
    if response.status_code != 200:
        print("Error al obtener información del servicio:", response.status_code)
        return None

    servicio_info = response.json()
    capas_disponibles = [capa["id"] for capa in servicio_info.get("layers", [])]

    if not capas_disponibles:
        return "No se encontraron capas disponibles en el servicio."

    features = []
    polygon_geometry = None

    if polygon_coords:
        polygon_geometry = {
            "rings": [polygon_coords],
            "spatialReference": {"wkid": 4326}
        }

    for capa in capas_disponibles:
        capa_url = f"{url}/{capa}/query"

        params = {
            "f": "geojson",
            "returnGeometry": "true",
            "outFields": "*",
        }

        if polygon_geometry:
            params.update({
                "spatialRel": "esriSpatialRelIntersects",
                "geometry": json.dumps(polygon_geometry),
                "geometryType": "esriGeometryPolygon",
                "inSR": 4326,
                "geometryPrecision": 5
            })
        else:
            params["where"] = "1=1"

        response = requests.get(capa_url, params=params)
        if response.status_code == 200:
            geojson_data = response.json()
            if "features" in geojson_data and geojson_data["features"]:
                features.extend(geojson_data["features"])
        else:
            print(f"Error al obtener datos de la capa {capa}: {response.status_code}")
    if download:
        with open("datos.geojson", "w", encoding="utf-8") as f:
            json.dump({"features": features}, f, indent=4, ensure_ascii=False)
        return "Archivo GeoJSON guardado como 'datos.geojson'"

    return features

# Ejemplo de uso
url_catastro = "https://mapas.igac.gov.co/server/rest/services/centrocontrol/EstacionesGNSS/MapServer"
polygon_coords = [
    [-74.18, 4.65],  # Punto 1
    [-74.16, 4.68],  # Punto 2
    [-74.10, 4.70],  # Punto 3
    [-74.05, 4.68],  # Punto 4
    [-74.06, 4.64],  # Punto 5
    [-74.10, 4.62],  # Punto 6
    [-74.15, 4.63]
]
datos = arcgis_query(url_catastro,polygon_coords,  CRS="EPSG:4326", download=False)
print(datos)