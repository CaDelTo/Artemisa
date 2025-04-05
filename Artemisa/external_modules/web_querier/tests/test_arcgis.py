from web_querier.data_web_querier import DataWebQuerier

def test_arcgis_query():
    web_querier = DataWebQuerier()
    data = web_querier.get_data(
        "arcgis",
        url="https://mapas.igac.gov.co/server/rest/services/centrocontrol/EstacionesGNSS/MapServer",
        polygon=[
            [-8249349.55, 516097.68],
            [-8247322.04, 519218.76],
            [-8239821.41, 521506.09],
            [-8233074.79, 519218.76],
            [-8234291.47, 514285.21],
            [-8239821.41, 512023.23],
            [-8246000.44, 513917.79]
        ],
        CRS="EPSG:3857"
    )  

    print("Datos obtenidos:", data)
    assert isinstance(data, list)
    assert len(data) > 0
