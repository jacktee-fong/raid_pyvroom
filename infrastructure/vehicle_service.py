from .interfaces.vehicle_service_interface import VehicleServiceInterface
import vroom
from typing import Optional, Tuple, List

class VehicleService(VehicleServiceInterface):
    def add_vehicles(self, problem_instance: vroom.Input, max_vehicles: int,
                    depot: int = 0,
                    time_windows: Optional[Tuple[int, int]] = None,
                    skills: Optional[List] = None,
                    capacity: Optional[List[int]] = None) -> None:
        if max_vehicles <= 0:
            return
        
        for i in range(max_vehicles):
            vehicle = vroom.Vehicle(
                id=i + 1,
                start=depot,
                end=depot
            )
            
            if time_windows is not None:
                vehicle.time_window = time_windows
            
            if skills is not None:
                vehicle.skills = skills
            
            if capacity is not None:
                vehicle.capacity = capacity
            
            problem_instance.add_vehicle(vehicle) 