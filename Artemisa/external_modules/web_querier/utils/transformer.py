from pyproj import Transformer

def transform_coordinates(coords, from_crs, target_crs):
    """
    Transforma coordenadas de un CRS a otro.

    Parámetros:
        coords (list | tuple): Lista de coordenadas [[lon, lat], [lon, lat], ...] o (lon_min, lat_min, lon_max, lat_max).
        from_crs (str): Código EPSG de origen.
        target_crs (str): Código EPSG de destino.

    Retorna:
        list | tuple: Lista de coordenadas transformadas o una tupla de valores transformados.
    """
    transformer = Transformer.from_crs(from_crs, target_crs, always_xy=True)

    if isinstance(coords, list):  # Para ArcGIS y WFS (lista de puntos)
        return [transformer.transform(lon, lat) for lon, lat in coords]
    elif isinstance(coords, tuple) and len(coords) == 4:  # Para WMS (bbox)
        lon_min, lat_min = transformer.transform(coords[0], coords[1])
        lon_max, lat_max = transformer.transform(coords[2], coords[3])
        return lon_min, lat_min, lon_max, lat_max
    else:
        raise ValueError("Formato de coordenadas no reconocido")
