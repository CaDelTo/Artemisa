import requests
from io import BytesIO
from PIL import Image
from web_querier.utils import transform_coordinates
from web_querier.strategies.base_strategy import BaseStrategy

class WMSStrategy(BaseStrategy):
    
    def get_data(self, url, image_size=(700, 400), CRS="EPSG:4326", download=False, lat_min=None, lon_min=None, lat_max=None, lon_max=None):
        url = url + "/export"

        if None in (lat_min, lon_min, lat_max, lon_max):
            bbox = "-180,-90,180,90"
            bbox_sr = "4326"
            image_sr = "4326"
        else:
            if CRS not in ["EPSG:3857", "EPSG:102100"]:
                lon_min, lat_min, lon_max, lat_max = transform_coordinates(
                    (lon_min, lat_min, lon_max, lat_max), CRS, "EPSG:3857"
                )
            bbox = f"{lon_min},{lat_min},{lon_max},{lat_max}"
            bbox_sr = "102100"
            image_sr = "102100"

        params = {
            "dpi": 96,
            "transparent": "true",
            "format": "tiff",
            "bbox": bbox,
            "bboxSR": bbox_sr,
            "imageSR": image_sr,
            "size": f"{image_size[0]},{image_size[1]}",
            "f": "image"
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            image_bytes = response.content
            image = Image.open(BytesIO(image_bytes))

            if download:
                file_name = "wms_image.tiff"
                image.save(file_name, format="TIFF")
                return f"Image saved as {file_name}"
            else:
                return image_bytes
        else:
            return "Error getting image from WMS service."
