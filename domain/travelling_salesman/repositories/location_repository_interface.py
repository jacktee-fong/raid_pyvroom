from abc import ABC, abstractmethod
from typing import List
from domain.travelling_salesman.entities.location import Location


class LocationRepositoryInterface(ABC):
    @abstractmethod
    def get_all_locations(self) -> List[Location]:
        """Retrieve all locations"""
        pass
    
    @abstractmethod
    def save_locations(self, locations: List[Location]) -> None:
        """Save locations"""
        pass 