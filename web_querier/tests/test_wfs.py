from web_querier.strategies.wfs_strategy import WFSStrategy

def test_wfs_query():
    url = "https://mapas2.igac.gov.co/server/rest/services/geodesia/redgravimetrica/MapServer"
    polygon_coords = [
        [-74.12, 4.65],
        [-74.16, 4.68],
        [-74.10, 4.70]
    ]
    wfs = WFSStrategy()
    data = wfs.get_data(url, polygon=polygon_coords, crs="EPSG:4326")
    print(data)
    assert isinstance(data, list)  # Asegurar que el resultado es una lista
    assert len(data) > 0  # Asegurar que hay datos
