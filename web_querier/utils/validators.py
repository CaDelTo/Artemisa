def validate_polygon(polygon):
    if not isinstance(polygon, list):
        raise ValueError("Polygon must be a list of coordinates.")
    
    for point in polygon:
        if not (isinstance(point, (list, tuple)) and len(point) == 2):
            raise ValueError("Each point in polygon must be a list or tuple of two coordinates (lon, lat).")
    
    return True

def validate_bbox(lat_min, lon_min, lat_max, lon_max):
    if None in (lat_min, lon_min, lat_max, lon_max):
        return False  # Se usa bbox global por defecto
    
    if not (-90 <= lat_min <= 90 and -90 <= lat_max <= 90):
        raise ValueError("Latitude values must be between -90 and 90.")
    
    if not (-180 <= lon_min <= 180 and -180 <= lon_max <= 180):
        raise ValueError("Longitude values must be between -180 and 180.")
    
    if lat_min >= lat_max or lon_min >= lon_max:
        raise ValueError("Minimum coordinates must be smaller than maximum coordinates.")
    
    return True
