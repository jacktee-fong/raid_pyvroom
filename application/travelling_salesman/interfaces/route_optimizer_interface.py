from abc import ABC, abstractmethod
from typing import List, Optional, Literal
from domain.travelling_salesman.entities.location import Location
from domain.travelling_salesman.entities.route import Route
from dataclasses import dataclass


@dataclass
class OptimizedRoute:
    vehicle_id: int
    locations: List[Location]
    total_distance: Optional[float]
    total_time: Optional[float]
    arrival_times: List[int]
    service_times: List[int]
    waiting_times: List[int]


class RouteOptimizerInterface(ABC):
    @abstractmethod
    def optimize_routes(
        self,
        locations: List[Location],
        max_vehicles: Optional[int] = None,
        depot_location: Optional[Location] = None,
        matrix_type: Literal["duration", "distance"] = "duration"
    ) -> List[Route]:
        """
        Optimize routes for given locations
        Args:
            locations: List of locations to visit
            max_vehicles: Maximum number of vehicles to use
            depot_location: Starting/ending location for vehicles
            matrix_type: Type of matrix to use for optimization ("duration" or "distance")
        Returns:
            List of optimized routes
        """
        pass
