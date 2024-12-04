from abc import ABC, abstractmethod
import vroom
from typing import Optional, Tuple, List

class VehicleServiceInterface(ABC):
    @abstractmethod
    def add_vehicles(self, 
                    problem_instance: vroom.Input,
                    max_vehicles: int,
                    depot: int = 0,
                    time_windows: Optional[Tuple[int, int]] = None,
                    skills: Optional[List] = None,
                    capacity: Optional[List[int]] = None) -> None:
        """Add vehicles to the problem instance with specified configurations."""
        pass 