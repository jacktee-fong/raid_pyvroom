from dataclasses import dataclass
from typing import Optional
from domain.travelling_salesman.value_objects.coordinates import Coordinates
from domain.travelling_salesman.value_objects.address import Address


@dataclass
class Location:
    id: int
    address: Address
    coordinates: Optional[Coordinates] = None
    
    def __str__(self) -> str:
        return f"Location(id={self.id}, address={self.address})" 