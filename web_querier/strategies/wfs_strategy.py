import requests
import json
from web_querier.utils.transformer import transform_coordinates
from web_querier.utils.validators import validate_polygon
from web_querier.strategies.base_strategy import BaseStrategy

class WFSStrategy(BaseStrategy):

    def get_data(self, url, polygon, crs="EPSG:3857", download=False):
        
        if validate_polygon(polygon) and crs not in ["EPSG:3857", "EPSG:102100"]:
            polygon = transform_coordinates(polygon, crs, "EPSG:3857")

        response = requests.get(f"{url}?f=json")
        if response.status_code != 200:
            return f"Error al obtener información del servicio: {response.status_code}"

        service_info = response.json()
        available_layers = [layer["id"] for layer in service_info.get("layers", [])]

        if not available_layers:
            return "No se encontraron capas en el servicio."

        data_dict = {}

        polygon_geometry = None
        if polygon:
            polygon_geometry = {
                "rings": [polygon],
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
                print(f"Error al obtener datos de la capa {layer}: {response.status_code}")
                data_dict[f"layer_{layer}"] = {}

        features = [data_dict[layer]["features"] for layer in data_dict if "features" in data_dict[layer] and data_dict[layer]["features"]]

        if download:
            geojson = {
                "features": [feature for sublist in features for feature in sublist]
            }
            with open("WFS_data.geojson", "w", encoding="utf-8") as f:
                json.dump(geojson, f, indent=4, ensure_ascii=False)
            return "Archivo GeoJSON guardado como 'WFS_data.geojson'"

        return features
