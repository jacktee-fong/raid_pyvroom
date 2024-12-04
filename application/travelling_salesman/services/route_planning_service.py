from typing import List, Optional, Literal
from domain.travelling_salesman.entities.location import Location
from application.travelling_salesman.use_cases.load_locations_use_case import LoadLocationsUseCase
from application.travelling_salesman.use_cases.get_optimal_routes_use_case import GetOptimalRoutesUseCase
from application.travelling_salesman.interfaces.route_optimizer_interface import OptimizedRoute
from domain.travelling_salesman.entities.route import Route


class RoutePlanningService:
    def __init__(
        self,
        load_locations_use_case: LoadLocationsUseCase,
        get_optimal_routes_use_case: GetOptimalRoutesUseCase
    ):
        self._load_locations_use_case = load_locations_use_case
        self._get_optimal_routes_use_case = get_optimal_routes_use_case
    
    def plan_routes(
        self,
        max_vehicles: Optional[int] = None,
        matrix_type: Literal["duration", "distance"] = "duration"
    ) -> List[Route]:
        """
        Plan optimal routes for delivery locations
        Args:
            max_vehicles: Maximum number of vehicles to use
            matrix_type: Type of matrix to use for optimization ("duration" or "distance")
        Returns:
            List of optimized routes
        """
        # Load locations from repository
        locations = self._load_locations_use_case.execute()
        
        # Get optimal routes
        routes = self._get_optimal_routes_use_case.execute(
            locations=locations,
            max_vehicles=max_vehicles,
            matrix_type=matrix_type
        )
        
        return routes 