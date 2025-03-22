import requests
import json
from web_querier.utils.transformer import transform_coordinates
from web_querier.utils.validators import validate_polygon
from web_querier.strategies.base_strategy import BaseStrategy

class ArcGisStrategy(BaseStrategy):

    def get_data(self, url, polygon=None, CRS="EPSG:4326", download=False):
        

        if validate_polygon(polygon) and CRS != "EPSG:4326":
            polygon = transform_coordinates(polygon, CRS, "EPSG:4326")

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

        if polygon:
            polygon_geometry = {
                "rings": [polygon],
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