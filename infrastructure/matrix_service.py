from typing import List, Tuple
import numpy as np
from domain.travelling_salesman.entities.location import Location
from infrastructure.onemap_service import OneMapService

class MatrixService:
    def __init__(self, onemap_service: OneMapService):
        self.onemap_service = onemap_service

    def get_matrices(self, locations: List[Location], matrix_type: str) -> Tuple[np.ndarray, np.ndarray]:

        duration_matrix, distance_matrix = self.onemap_service.get_route_matrices(
            [(loc.coordinates.latitude, loc.coordinates.longitude) for loc in locations]
        )
        print(locations)
        return duration_matrix, distance_matrix 