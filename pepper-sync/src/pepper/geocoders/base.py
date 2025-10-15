from abc import ABC, abstractmethod
from pepper import config

from pepper.types import GeocodeOption


class BaseGeocoder(ABC):
    options: GeocodeOption

    def __init__(self) -> None:
        self.options = config.options.geocode or GeocodeOption()
        
    @abstractmethod
    def get_address(self, lat: float, lon: float) -> str | None:
        pass
