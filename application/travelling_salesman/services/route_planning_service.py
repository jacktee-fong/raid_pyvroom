from typing import List, Optional
from domain.travelling_salesman.entities.location import Location
from domain.travelling_salesman.entities.route import Route
from application.travelling_salesman.use_cases.get_optimal_routes_use_case import GetOptimalRoutesUseCase


class RoutePlanningService:
    def __init__(self, load_locations_use_case, get_optimal_routes_use_case: GetOptimalRoutesUseCase):
        self._load_locations_use_case = load_locations_use_case
        self._get_optimal_routes_use_case = get_optimal_routes_use_case
    
    def plan_routes(
        self,
        max_vehicles: int,
        matrix_type: str,
        depot_location: Optional[Location] = None
    ) -> (List[Route], List[Location]):
        """
        Plan routes for the traveling salesman problem
        Args:
            max_vehicles: Maximum number of vehicles to use
            matrix_type: Type of matrix to use for optimization
            depot_location: Optional depot location
        Returns:
            Tuple of (optimized_routes, unassigned_locations)
        """
        # Load locations
        locations = self._load_locations_use_case.execute()
        
        # Get optimal routes
        optimized_routes = self._get_optimal_routes_use_case.execute(
            locations=locations,
            max_vehicles=max_vehicles,
            matrix_type=matrix_type
        )
        
        # Determine unassigned locations
        assigned_location_ids = {loc.id for route in optimized_routes for loc in route.locations}
        unassigned_locations = [loc for loc in locations if loc.id not in assigned_location_ids]
        
        return optimized_routes, unassigned_locations 