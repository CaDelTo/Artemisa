from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    
    @abstractmethod
    def get_data(self, url, polygon):
        pass