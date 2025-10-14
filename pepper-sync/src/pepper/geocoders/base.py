from abc import ABC, abstractmethod


class BaseGeocoder(ABC):
    @abstractmethod
    def get_address(lat: float, lon: float) -> str:
        pass
