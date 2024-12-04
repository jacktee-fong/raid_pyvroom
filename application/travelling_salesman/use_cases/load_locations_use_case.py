from typing import List
from domain.travelling_salesman.entities.location import Location
from domain.travelling_salesman.repositories.location_repository_interface import LocationRepositoryInterface


class LoadLocationsUseCase:
    def __init__(self, location_repository: LocationRepositoryInterface):
        self._location_repository = location_repository
    
    def execute(self) -> List[Location]:
        """
        Load all locations from the repository
        Returns:
            List of Location entities
        """
        return self._location_repository.get_all_locations() 