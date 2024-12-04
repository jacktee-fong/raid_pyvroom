from dataclasses import dataclass
from typing import List
from .location_dto import LocationDTO

@dataclass
class RouteDTO:
    vehicle_id: int
    locations: List[LocationDTO]
    total_distance: float
    total_time: float 