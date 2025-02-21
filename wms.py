import requests
from io import BytesIO
from PIL import Image
from pyproj import Transformer

def wms_query(lat_min, lon_min, lat_max, lon_max, wms_url, image_size, CRS, download):
    """
    Obtiene una imagen de un servicio WMS dado un BBox en coordenadas WGS 84.

    Parámetros:
        lat_min (float): Latitud mínima (esquina inferior izquierda).
        lon_min (float): Longitud mínima (esquina inferior izquierda).
        lat_max (float): Latitud máxima (esquina superior derecha).
        lon_max (float): Longitud máxima (esquina superior derecha).
        wms_url (str): URL del servicio WMS.
        image_size (tuple): Tamaño de la imagen en píxeles (ancho, alto).
        CRS (str): Código EPSG del sistema de referencia de coordenadas.
        download (bool): Indica si la imagen debe guardarse localmente.

    Retorna:
        bytes o str: Bytes de la imagen si `download` es False.
                     Mensaje de confirmación si `download` es True.
    """
    wms_url = wms_url + "/export"

    if CRS != "EPSG:3857" or CRS != "EPSG:102100":
        transformer = Transformer.from_crs(CRS, "EPSG:3857", always_xy=True)
        lat_min, lon_min = transformer.transform(lon_min, lat_min)
        lat_max, lon_max = transformer.transform(lon_max, lat_max)

    params = {
        "dpi": 96,
        "transparent": "true",
        "format": "tiff",
        "bbox": f"{lat_min},{lon_min},{lat_max},{lon_max}",
        "bboxSR": "102100",
        "imageSR": "102100",
        "size": f"{image_size[0]},{image_size[1]}",
        "f": "image"
    }

    response = requests.get(wms_url, params=params)

    file_name = "wms_image.tiff"
    if response.status_code == 200:
        image_bytes = response.content
        image = Image.open(BytesIO(image_bytes))

        if download:
            image.save(file_name, format="TIFF")
            return f"Imagen guardada como {file_name}"
        else:
            return image_bytes
    else:
        print("Error al obtener la imagen del WMS.")
        return None

# Ejemplo de uso
wms_url = "https://mapas2.igac.gov.co/server/rest/services/geodesia/redpasivacem/MapServer"
image = wms_query(8.5, -75.0, 1.0, -74.5, wms_url, (700, 400),"EPSG:4326", True)
