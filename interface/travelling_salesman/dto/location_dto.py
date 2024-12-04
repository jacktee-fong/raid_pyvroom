from dataclasses import dataclass

@dataclass
class LocationDTO:
    job_id: int
    postal_code: str
    address: str 