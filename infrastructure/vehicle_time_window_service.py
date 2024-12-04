import vroom
from typing import List, Optional
from domain.vehicle_time_windows.entities.vehicle import Vehicle
from domain.travelling_salesman.entities.location import Location

class VehicleTimeWindowService:
    def add_vehicles(
        self,
        problem_instance: vroom.Input,
        vehicles: List[Vehicle],
        depot_location: Optional[Location] = None
    ) -> None:
        """Add vehicles with time windows to the VROOM problem instance"""
        for vehicle in vehicles:
            vroom_vehicle = vroom.Vehicle(
                id=vehicle.id,
                start=0,  # Depot is always at index 0
                end=0,    # Return to depot
                time_window=(vehicle.time_window.start, vehicle.time_window.end)
            )
            problem_instance.add_vehicle(vroom_vehicle) 