from dataclasses import dataclass
from domain.vehicle_time_windows.value_objects.time_window import TimeWindow

@dataclass
class Vehicle:
    """
    Represents a delivery vehicle with time windows
    """
    id: int
    time_window: TimeWindow
    
    def __post_init__(self):
        """
        Validate vehicle data after initialization
        """
        if not isinstance(self.id, int):
            raise ValueError("id must be an integer")
        
        if not isinstance(self.time_window, TimeWindow):
            raise ValueError("time_window must be a TimeWindow instance")

    def __str__(self) -> str:
        return f"Vehicle(id={self.id}, time_window={self.time_window})"