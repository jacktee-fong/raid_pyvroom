from typing import List, Optional
from domain.travelling_salesman.entities.location import Location
from application.travelling_salesman.interfaces.route_optimizer_interface import OptimizedRoute
import pandas as pd

class SolutionProcessorService:
    def process_solution(self, solution, locations: List[Location], depot_location: Optional[Location] = None) -> List[OptimizedRoute]:
        optimized_routes = []
        fulfilled_job_ids = set()
        
        # Convert solution.routes to DataFrame
        vehicle_groups = pd.DataFrame(solution.routes).groupby('vehicle_id')
        print(solution.routes)
        
        for vehicle_id, vehicle_steps in vehicle_groups:
            route_locations = []
            arrival_times = []
            service_times = []
            waiting_times = []
            
            # Add depot location at start if provided
            if depot_location:
                route_locations.append(depot_location)
            
            # Sort steps by arrival time to ensure correct order
            sorted_steps = vehicle_steps.sort_values('arrival')
            
            # Add locations based on job IDs
            for _, step in sorted_steps.iterrows():
                if step['type'] == 'job':
                    location_index = step['id'] - 1
                    if 0 <= location_index < len(locations):
                        route_locations.append(locations[location_index])
                        arrival_times.append(step['arrival'])
                        service_times.append(step['service'])
                        waiting_times.append(step['waiting_time'])
                        fulfilled_job_ids.add(step['id'])
            
            # Add depot location at end if provided
            if depot_location:
                route_locations.append(depot_location)
            
            # Calculate total duration and distance from the last step
            total_time = sorted_steps['duration'].sum()
            total_distance = sorted_steps['duration'].sum() * 10  # Example calculation
            
            optimized_routes.append(OptimizedRoute(
                vehicle_id=vehicle_id,
                locations=route_locations,
                total_distance=total_distance,
                total_time=total_time,
                arrival_times=arrival_times,
                service_times=service_times,
                waiting_times=waiting_times
            ))
        
        # Determine unfulfilled jobs
        all_job_ids = set(range(1, len(locations)))  # Assuming job IDs are 1-indexed
        unfulfilled_job_ids = all_job_ids - fulfilled_job_ids
        
        # Output unfulfilled jobs
        print("Unfulfilled Job IDs:", unfulfilled_job_ids)
        
        return optimized_routes 