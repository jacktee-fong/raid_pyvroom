from dataclasses import dataclass

@dataclass(frozen=True)
class Address:
    postal_code: str
    full_address: str
    
    def __str__(self) -> str:
        return self.full_address 