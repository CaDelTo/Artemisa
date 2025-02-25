import requests
from io import BytesIO
from PIL import Image
from pyproj import Transformer

def wms_query(wms_url, image_size=(700, 400), CRS="EPSG:4326", download=False, lat_min=None, lon_min=None, lat_max=None, lon_max=None):
    """
    Gets an image from a WMS service given a BBox in WGS 84 coordinates.
    If no coordinates are provided, it gets the complete image of the service.

    Parameters:
        wms_url (str): Base URL of the WMS service.
        image_size (tuple, optional): Image size in pixels (width, height). Default (700, 400).
        CRS (str, optional): EPSG code of the coordinate reference system. Default "EPSG:4326".
        download (bool, optional): Indicates if the image should be saved locally. Default False.
        lat_min, lon_min, lat_max, lon_max (float, optional): Coordinates of the area of interest.

    Returns:
        bytes or str: Image bytes if `download` is False.
                     Confirmation message if `download` is True.
    """
    wms_url = wms_url + "/export"

    if None in (lat_min, lon_min, lat_max, lon_max):
        bbox = "-180,-90,180,90"
        bbox_sr = "4326"
        image_sr = "4326"
    else:
        if CRS != "EPSG:3857" and CRS != "EPSG:102100":
            transformer = Transformer.from_crs(CRS, "EPSG:3857", always_xy=True)
            lon_min, lat_min = transformer.transform(lon_min, lat_min)
            lon_max, lat_max = transformer.transform(lon_max, lat_max)

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

    response = requests.get(wms_url, params=params)

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

# Example of use
wms_url = "https://mapas2.igac.gov.co/server/rest/services/geodesia/redpasivacem/MapServer"
image = wms_query(wms_url, (700, 400), "EPSG:4326", False)
print(image)