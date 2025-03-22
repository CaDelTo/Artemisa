from web_querier.strategies.arcgis_strategy import ArcGisStrategy

def test_arcgis_query():
    url = "https://mapas.igac.gov.co/server/rest/services/centrocontrol/EstacionesGNSS/MapServer"
    polygon_coords = [
        [-8249349.55, 516097.68],  # Punto 1
        [-8247322.04, 519218.76],  # Punto 2
        [-8239821.41, 521506.09],  # Punto 3
        [-8233074.79, 519218.76],  # Punto 4
        [-8234291.47, 514285.21],  # Punto 5
        [-8239821.41, 512023.23],  # Punto 6
        [-8246000.44, 513917.79]   # Punto 7
    ]
    arcgis = ArcGisStrategy()
    data = arcgis.get_data(url, polygon=polygon_coords, CRS="EPSG:3857")
    
    print(data)  # Para ver qué devuelve
    assert isinstance(data, list)  # Asegurar que el resultado es una lista
    assert len(data) > 0  # Asegurar que hay datos
