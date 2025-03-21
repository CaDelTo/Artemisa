from .strategies import WMSStrategy, WFSStrategy, ArcGisStrategy

class DataWebQuerier:
    def __init__(self, strategy_type):
        """
        Inicializa el querier con una estrategia específica.

        Parámetros:
            strategy_type (str): Tipo de estrategia a usar ('wms', 'wfs' o 'arcgis').
        """
        self.strategy = self._get_strategy(strategy_type)

    def _get_strategy(self, strategy_type):
        """Devuelve la estrategia adecuada según el tipo proporcionado."""
        strategies = {
            "wms": WMSStrategy,
            "wfs": WFSStrategy,
            "arcgis": ArcGisStrategy
        }
        if strategy_type not in strategies:
            raise ValueError(f"Estrategia '{strategy_type}' no válida. Usa: {list(strategies.keys())}")
        return strategies[strategy_type]()

    def get_data(self, **kwargs):
        """
        Obtiene datos según la estrategia seleccionada.

        Parámetros:
            kwargs: Argumentos específicos de cada estrategia.

        Retorna:
            Datos obtenidos según la estrategia utilizada.
        """
        return self.strategy.get_data(**kwargs)
