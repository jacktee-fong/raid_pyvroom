from dataclasses import dataclass

@dataclass(frozen=True)
class TimeWindow:
    """
    Represents a time window with start and end times in seconds
    """
    start: int
    end: int
    
    def __post_init__(self):
        """
        Validate time window data after initialization
        """
        if not isinstance(self.start, int):
            raise ValueError("start must be an integer")
        
        if not isinstance(self.end, int):
            raise ValueError("end must be an integer")
        
        if self.start < 0:
            raise ValueError("start time cannot be negative")
        
        if self.end <= self.start:
            raise ValueError("end time must be greater than start time")
    
    def __str__(self) -> str:
        return f"TimeWindow(start={self.start}, end={self.end})"