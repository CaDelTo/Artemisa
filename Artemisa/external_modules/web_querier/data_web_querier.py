from .strategies.wms_strategy import WMSStrategy
from .strategies.wfs_strategy import WFSStrategy
from .strategies.arcgis_strategy import ArcGisStrategy

class DataWebQuerier:
    """
    Consulta datos desde una fuente web usando diferentes estrategias (WMS, WFS, ArcGIS).
    """

    def __init__(self):
        self.strategies = {
            "wms": WMSStrategy(),
            "wfs": WFSStrategy(),
            "arcgis": ArcGisStrategy(),
        }

    def get_data(self, strategy_type, **kwargs):
        """
        Obtiene datos usando la estrategia especificada.

        Args:
            strategy_type (str): Tipo de estrategia ('wms', 'wfs', 'arcgis').
            **kwargs: Parámetros específicos para cada estrategia.

        Returns:
            list: Datos obtenidos de la fuente.
        """
        if strategy_type not in self.strategies:
            raise ValueError(f"Estrategia no soportada: {strategy_type}")

        strategy = self.strategies[strategy_type]
        return strategy.get_data(**kwargs)
