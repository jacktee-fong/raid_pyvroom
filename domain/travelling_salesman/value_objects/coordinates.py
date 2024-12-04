from dataclasses import dataclass

@dataclass(frozen=True)
class Coordinates:
    latitude: float
    longitude: float
    
    def __str__(self) -> str:
        return f"({self.latitude}, {self.longitude})" 