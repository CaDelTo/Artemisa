from web_querier.data_web_querier import DataWebQuerier

def test_wfs_query():
    web_querier = DataWebQuerier()
    data = web_querier.get_data(
        "wfs",
        url="https://mapas2.igac.gov.co/server/rest/services/geodesia/redgravimetrica/MapServer",
        polygon=[
            [-74.12, 4.65],
            [-74.16, 4.68],
            [-74.10, 4.70]
        ],
        CRS="EPSG:4326"
    )  

    print("Datos obtenidos:", data)
    assert isinstance(data, list)
    assert len(data) > 0
