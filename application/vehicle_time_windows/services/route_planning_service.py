from typing import List, Optional, Literal
from domain.travelling_salesman.entities.location import Location
from domain.vehicle_time_windows.entities.vehicle import Vehicle
from domain.travelling_salesman.entities.route import Route
from application.travelling_salesman.use_cases.load_locations_use_case import LoadLocationsUseCase
from application.vehicle_time_windows.use_cases.get_optimal_routes_with_time_windows_use_case import GetOptimalRoutesWithTimeWindowsUseCase


class RoutePlanningService:
    def __init__(
        self,
        load_locations_use_case: LoadLocationsUseCase,
        get_optimal_routes_use_case: GetOptimalRoutesWithTimeWindowsUseCase
    ):
        self._load_locations_use_case = load_locations_use_case
        self._get_optimal_routes_use_case = get_optimal_routes_use_case
    
    def plan_routes(
        self,
        vehicles: List[Vehicle],
        matrix_type: Literal["duration", "distance"] = "duration",
        depot_location: Optional[Location] = None
    ) -> List[Route]:
        """
        Plan optimal routes for delivery locations with time windows
        Args:
            vehicles: List of vehicles to use
            matrix_type: Type of matrix to use for optimization ("duration" or "distance")
            depot_location: The depot location
        Returns:
            List of optimized routes
        """
        # Load delivery locations
        delivery_locations = self._load_locations_use_case.execute()
        
        # Combine depot with delivery locations for matrix calculation
        all_locations = [depot_location] + delivery_locations
        
        # Get optimal routes with time windows
        routes, unassigned = self._get_optimal_routes_use_case.execute(
            locations=all_locations,  # Pass all locations including depot
            vehicles=vehicles,
            matrix_type=matrix_type,
            depot_location=depot_location
        )
        
        return routes, unassigned 