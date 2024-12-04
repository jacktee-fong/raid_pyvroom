from typing import List, Optional, Literal
from domain.travelling_salesman.entities.location import Location
from domain.travelling_salesman.entities.route import Route
from application.travelling_salesman.interfaces.route_optimizer_interface import RouteOptimizerInterface


class GetOptimalRoutesUseCase:
    def __init__(self, route_optimizer: RouteOptimizerInterface):
        self._route_optimizer = route_optimizer
    
    def execute(
        self,
        locations: List[Location],
        max_vehicles: Optional[int] = None,
        matrix_type: Literal["duration", "distance"] = "duration"
    ) -> List[Route]:
        """
        Get optimal routes for given locations
        Args:
            locations: List of locations to visit
            max_vehicles: Maximum number of vehicles to use
            matrix_type: Type of matrix to use for optimization ("duration" or "distance")
        Returns:
            List of optimized routes
        """
        return self._route_optimizer.optimize_routes(
            locations=locations,
            max_vehicles=max_vehicles,
            matrix_type=matrix_type
        ) 