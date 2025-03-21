from web_querier.strategies.arcgis_strategy import ArcGisStrategy

def test_arcgis_query():
    url = "https://mapas.igac.gov.co/server/rest/services/centrocontrol/EstacionesGNSS/MapServer"
    polygon_coords = [
        [-74.18, 4.65],  # Punto 1
        [-74.16, 4.68],  # Punto 2
        [-74.10, 4.70],  # Punto 3
        [-74.05, 4.68],  # Punto 4
        [-74.06, 4.64],  # Punto 5
        [-74.10, 4.62],  # Punto 6
        [-74.15, 4.63]
    ]
    arcgis = ArcGisStrategy()
    data = arcgis.get_data(url, polygon=polygon_coords, CRS="EPSG:4326")
    
    print(data)  # Para ver qué devuelve
    assert isinstance(data, list)  # Asegurar que el resultado es una lista
    assert len(data) > 0  # Asegurar que hay datos
