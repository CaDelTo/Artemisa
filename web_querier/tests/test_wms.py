from web_querier.data_web_querier import DataWebQuerier

def test_wms_query():
    web_querier = DataWebQuerier()
    data = web_querier.get_data(
        "wms",
        url="https://mapas2.igac.gov.co/server/rest/services/geodesia/redpasivacem/MapServer",
        CRS="EPSG:4326",
        download=False
    )  

    print("Datos obtenidos:", data)
    assert isinstance(data, (list, bytes))
    assert len(data) > 0
