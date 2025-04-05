from retriever_service.data_retriever import DataRetriever

def test_data_retriever_wfs():
    retriever = DataRetriever()
    data = retriever.get_data(
        strategy_type="wfs",
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

