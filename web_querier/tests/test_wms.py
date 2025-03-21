from web_querier.strategies.wms_strategy import WMSStrategy

def test_wms_query():
    url = "https://mapas2.igac.gov.co/server/rest/services/geodesia/redpasivacem/MapServer"
    wms = WMSStrategy()
    data = wms.get_data(url, image_size=(700, 400), CRS="EPSG:4326", download=False)
    
    print(data)  # Para ver qué devuelve
    assert isinstance(data, bytes)  # Asegurar que la respuesta es en bytes (imagen)
    assert len(data) > 0  # Asegurar que hay datos
