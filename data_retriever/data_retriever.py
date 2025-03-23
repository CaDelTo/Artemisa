from web_querier.data_web_querier import DataWebQuerier

class DataRetriever:

    def __init__(self):
        self.web_querier = DataWebQuerier()
    
    def get_data(self, **kwargs):
        """
        Obtiene datos de una fuente de datos geoespaciales.

        Parámetros:
            source (str): Fuente de datos ('wms', 'wfs' o 'arcgis').
            polygon (list): Coordenadas del polígono en formato GeoJSON.

        Retorna:
            Datos obtenidos de la fuente de datos.
        """
        return self.web_querier.get_data(**kwargs)