import pandas as pd
from typing import List
import re
from domain.travelling_salesman.entities.location import Location
from domain.travelling_salesman.repositories.location_repository_interface import LocationRepositoryInterface
from domain.travelling_salesman.value_objects.address import Address
from infrastructure.onemap_service import OneMapService


class ExcelLocationRepository(LocationRepositoryInterface):
    def __init__(self, file_path: str):
        self._file_path = file_path
        self._onemap_service = OneMapService()
    
    def get_all_locations(self) -> List[Location]:
        """
        Retrieve all locations from the Excel file
        Returns:
            List of Location entities
        """
        df = pd.read_excel(self._file_path)
        locations = []
        
        for index, row in df.iterrows():
            full_address = row['address']
            
            # Extract postal code using regex
            postal_code_match = re.search(r'\b\d{6}\b', full_address)
            if postal_code_match:
                postal_code = postal_code_match.group(0)
            else:
                print(f"Warning: Could not extract postal code from address: {full_address}")
                continue
            
            address = Address(postal_code=postal_code, full_address=full_address)
            location = Location(id=row['job_id'], address=address)
            
            # Get coordinates from OneMap service
            coordinates = self._onemap_service.get_coordinates(postal_code)
            if coordinates:
                location.coordinates = coordinates
            
            locations.append(location)
        
        return locations
    
    def save_locations(self, locations: List[Location]) -> None:
        """
        Save locations to the Excel file
        """
        data = [{'job_id': loc.id, 'address': loc.address.full_address} for loc in locations]
        df = pd.DataFrame(data)
        df.to_excel(self._file_path, index=False) 