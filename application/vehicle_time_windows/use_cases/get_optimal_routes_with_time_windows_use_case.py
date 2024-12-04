from typing import List, Optional, Literal, Tuple
from domain.travelling_salesman.entities.location import Location
from domain.vehicle_time_windows.entities.vehicle import Vehicle
from domain.travelling_salesman.entities.route import Route
from application.vehicle_time_windows.interfaces.route_optimizer_interface import RouteOptimizerInterface


class GetOptimalRoutesWithTimeWindowsUseCase:
    def __init__(self, route_optimizer: RouteOptimizerInterface):
        self._route_optimizer = route_optimizer
    
    def execute(
        self,
        locations: List[Location],
        vehicles: List[Vehicle],
        depot_location: Optional[Location] = None,
        matrix_type: Literal["duration", "distance"] = "duration"
    ) -> Tuple[List[Route], List[Location]]:
        """
        Get optimal routes for given locations and vehicles with time windows
        Args:
            locations: List of locations to visit
            vehicles: List of vehicles with time windows
            depot_location: Optional depot location
            matrix_type: Type of matrix to use for optimization ("duration" or "distance")
        Returns:
            Tuple of (optimized_routes, unassigned_locations)
        """
        print("Executing route optimization...")
        print(f"Locations: {len(locations)} locations")
        print(f"Vehicles: {len(vehicles)} vehicles")
        print(f"Depot Location: {depot_location}")
        print(f"Matrix Type: {matrix_type}")
        
        optimized_routes = self._route_optimizer.optimize_routes(
            locations=locations,
            vehicles=vehicles,
            depot_location=depot_location,
            matrix_type=matrix_type
        )
        
        # Get unassigned locations
        assigned_location_ids = set()
        for route in optimized_routes:
            for location in route.locations:
                assigned_location_ids.add(location.id)
        
        unassigned_locations = [
            loc for loc in locations 
            if loc.id not in assigned_location_ids and loc.id != depot_location.id
        ]
        
        print(f"Optimization complete. {len(optimized_routes)} routes created.")
        print(f"Unassigned locations: {len(unassigned_locations)}")
        
        return optimized_routes, unassigned_locations 