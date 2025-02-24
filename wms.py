import requests
from io import BytesIO
from PIL import Image
from pyproj import Transformer

def wms_query(wms_url, image_size=(700, 400), CRS="EPSG:4326", download=False, lat_min=None, lon_min=None, lat_max=None, lon_max=None):
    """
    Obtiene una imagen de un servicio WMS dado un BBox en coordenadas WGS 84.
    Si no se proporcionan coordenadas, obtiene la imagen completa del servicio.

    Parámetros:
        wms_url (str): URL base del servicio WMS.
        image_size (tuple, opcional): Tamaño de la imagen en píxeles (ancho, alto). Por defecto (700, 400).
        CRS (str, opcional): Código EPSG del sistema de referencia de coordenadas. Por defecto "EPSG:4326".
        download (bool, opcional): Indica si la imagen debe guardarse localmente. Por defecto False.
        lat_min, lon_min, lat_max, lon_max (float, opcional): Coordenadas del área de interés.

    Retorna:
        bytes o str: Bytes de la imagen si `download` es False.
                     Mensaje de confirmación si `download` es True.
    """
    wms_url = wms_url + "/export"

    if None in (lat_min, lon_min, lat_max, lon_max):
        bbox = "-180,-90,180,90"
        bboxSR = "4326"
        imageSR = "4326"
    else:
        if CRS != "EPSG:3857" and CRS != "EPSG:102100":
            transformer = Transformer.from_crs(CRS, "EPSG:3857", always_xy=True)
            lon_min, lat_min = transformer.transform(lon_min, lat_min)
            lon_max, lat_max = transformer.transform(lon_max, lat_max)

        bbox = f"{lon_min},{lat_min},{lon_max},{lat_max}"
        bboxSR = "102100"
        imageSR = "102100"

    params = {
        "dpi": 96,
        "transparent": "true",
        "format": "tiff",
        "bbox": bbox,
        "bboxSR": bboxSR,
        "imageSR": imageSR,
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
            return f"Imagen guardada como {file_name}"
        else:
            return image_bytes
    else:
        print("Error al obtener la imagen del WMS.")
        return None

# Ejemplo de uso
wms_url = "https://mapas2.igac.gov.co/server/rest/services/geodesia/redpasivacem/MapServer"
image = wms_query(wms_url, (700, 400),"EPSG:4326", True)