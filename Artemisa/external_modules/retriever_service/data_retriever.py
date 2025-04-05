from external_modules.web_querier.data_web_querier import DataWebQuerier

class DataRetriever:

    def __init__(self):
        self.web_querier = DataWebQuerier()
        #TODO: Implementar self.db_querier = DataDBQuerier()
    
    def get_data(self, **kwargs):
        """
        Obtiene datos de una fuente de datos geoespaciales.

        Parámetros:
            source (str): Fuente de datos ('wms', 'wfs' o 'arcgis').
            polygon (list): Coordenadas del polígono en formato GeoJSON.

        Retorna:
            Datos obtenidos de la fuente de datos.
        """
        try:
            data = self.web_querier.get_data(**kwargs)
            return data
        except ValueError as e:
            return str(e)
        
        #TODO: Implementar except para DataDBQuerier
        return 