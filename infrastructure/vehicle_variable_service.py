import vroom
from typing import List, Optional
from domain.vehicle_time_windows.entities.vehicle import Vehicle
from domain.travelling_salesman.entities.location import Location

class VehicleVariableService:
    def add_vehicles(
        self,
        problem_instance: vroom.Input,
        vehicles: List[Vehicle],
        depot_location: Optional[Location] = None
    ) -> None:
        """Add vehicles with time windows to the VROOM problem instance"""
        depot_index = 0  # Default to index 0 if no depot location is provided
        if depot_location:
            depot_index = depot_location.id

        for vehicle in vehicles:
            vroom_vehicle = vroom.Vehicle(
                id=vehicle.id,
                start=depot_index,  # Use depot index
                end=depot_index,    # Return to depot
                time_window=(vehicle.time_window.start, vehicle.time_window.end)
            )
            problem_instance.add_vehicle(vroom_vehicle) 