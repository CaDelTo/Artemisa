from .strategies.arcgis import arcgis_query
from .strategies.wfs import wfs_query
from .strategies.wms import wms_query

class DataWebQuerier:
    def __init__ (self):
        self.strategies = {
            'arcgis': arcgis_query,
            'wfs': wfs_query,
            'wms': wms_query
        }
    def get(self, source, polygon, dataType):
        strategy = self.strategies.get(source)
        if not strategy:
            return 'Invalid source'
        return strategy(source, polygon)