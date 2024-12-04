from typing import List, Optional
import folium
from domain.travelling_salesman.entities.location import Location
from domain.travelling_salesman.value_objects.coordinates import Coordinates
from helper.onemap import OneMapQuery

class OneMapService:
    def __init__(self):
        self._onemap_query = OneMapQuery()
        self._onemap_query.get_onemap_token()
    
    def get_coordinates(self, postal_code: str) -> Optional[Coordinates]:
        """
        Get coordinates for a postal code using OneMap
        Args:
            postal_code: The postal code to look up
        Returns:
            Coordinates object or None if not found
        """
        latlong = self._onemap_query.get_postal_latlong(postal_code)
        if latlong:
            return Coordinates(latitude=latlong[0], longitude=latlong[1])
        return None
    
    def plot_routes(self, routes: List[List[Location]], output_file: str) -> None:
        """
        Plot routes on a map and save to an HTML file
        Args:
            routes: List of routes, each route is a list of Location entities
            output_file: Path to the output HTML file
        """
        # Initialize map centered around Singapore
        map_obj = folium.Map(location=[1.352083, 103.819839], zoom_start=12, tiles="cartodbpositron")
        
        # Plot each route
        for color_index, route in enumerate(routes, start=1):
            for i in range(len(route) - 1):
                start_location = route[i]
                end_location = route[i + 1]
                
                if start_location.coordinates and end_location.coordinates:
                    self._onemap_query.plot_routes(
                        start_latlong=(start_location.coordinates.latitude, start_location.coordinates.longitude),
                        end_latlong=(end_location.coordinates.latitude, end_location.coordinates.longitude),
                        map_obj=map_obj,
                        color_index=color_index,
                        sequence=(i, i+1)
                    )
        
        # Save map to HTML
        map_obj.save(output_file) 