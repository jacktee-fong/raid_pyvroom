from dataclasses import dataclass
from typing import List
from domain.travelling_salesman.entities.location import Location

@dataclass
class Route:
    """
    Represents an optimized delivery route
    """
    vehicle_id: int
    locations: List[Location]
    total_distance: float
    total_time: float
    sequence_numbers: List[int]

    def __post_init__(self):
        """
        Validate route data after initialization
        """
        if not isinstance(self.vehicle_id, int):
            raise ValueError("vehicle_id must be an integer")
        
        if not isinstance(self.locations, list):
            raise ValueError("locations must be a list")
        
        if not all(isinstance(loc, Location) for loc in self.locations):
            raise ValueError("all locations must be Location instances")
        
        if not isinstance(self.total_distance, (int, float)):
            raise ValueError("total_distance must be a number")
        
        if not isinstance(self.total_time, (int, float)):
            raise ValueError("total_time must be a number") 