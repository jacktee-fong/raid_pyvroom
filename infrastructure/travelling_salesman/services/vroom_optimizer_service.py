from typing import List, Optional, Literal
import vroom
from domain.travelling_salesman.entities.location import Location
from domain.travelling_salesman.value_objects.address import Address
from domain.travelling_salesman.value_objects.coordinates import Coordinates
from application.travelling_salesman.interfaces.route_optimizer_interface import RouteOptimizerInterface, OptimizedRoute
from helper.debug_utils import debug_print
from helper.onemap import OneMapQuery
from domain.travelling_salesman.entities.route import Route


class VroomOptimizerService(RouteOptimizerInterface):
    def __init__(self):
        self.onemap = OneMapQuery()

    def optimize_routes(
        self,
        locations: List[Location],
        max_vehicles: Optional[int] = None,
        depot_location: Optional[Location] = None,
        matrix_type: Literal["duration", "distance"] = "duration"
    ) -> List[OptimizedRoute]:
        """
        Optimize routes using VROOM with OneMap matrices
        """
        try:
            debug_print("Step 1: Starting optimization", prefix="VROOM-STEP")
            
            # Set default depot if none provided
            if not depot_location:
                debug_print("Setting default depot location (338729)", prefix="VROOM-STEP")
                depot_coords = self.onemap.get_postal_latlong("338729")
                if not depot_coords:
                    raise ValueError("Could not get coordinates for depot postal code 338729")
                
                # Create depot location with proper Address object
                depot_location = Location(
                    id=0,  # Use 0 for depot
                    coordinates=Coordinates(latitude=depot_coords[0], longitude=depot_coords[1]),
                    address=Address(
                        postal_code="338729",
                        full_address="Default Depot (338729)",
                    )
                )
            
            # Add depot to start of locations list (ensure it's always first)
            locations = [depot_location] + [loc for loc in locations if loc.id != depot_location.id]

            # Create a unique list of coordinates and map location IDs to indices
            unique_coords = {}
            coords_list = []
            for loc in locations:
                # Handle coordinates whether they're a tuple or a Coordinates object
                if isinstance(loc.coordinates, tuple):
                    coord_tuple = loc.coordinates
                else:
                    coord_tuple = (loc.coordinates.latitude, loc.coordinates.longitude)
                
                if coord_tuple not in unique_coords:
                    unique_coords[coord_tuple] = len(coords_list)
                    coords_list.append(coord_tuple)

            # Initialize OneMap service and get matrices
            debug_print("Step 2: Getting matrices from OneMap", prefix="VROOM-STEP")
            duration_matrix, distance_matrix = self.onemap.get_route_matrices(coords_list)
            
            # Initialize VROOM problem
            debug_print("Step 3: Initializing VROOM problem", prefix="VROOM-STEP")
            problem_instance = vroom.Input()
            
            # Set matrix
            debug_print("Step 4: Setting distance/duration matrix", prefix="VROOM-STEP")
            if matrix_type == "duration":
                problem_instance.set_durations_matrix(profile="car", matrix_input=duration_matrix.tolist())
            else:
                problem_instance.set_durations_matrix(profile="car", matrix_input=distance_matrix.tolist())
            
            # Add vehicles
            debug_print("Step 5: Adding vehicles", prefix="VROOM-STEP")
            vehicle_count = max_vehicles if max_vehicles else 1
            for i in range(vehicle_count):
                vehicle = vroom.Vehicle(
                    id=i + 1,
                    start=0,  # Depot is always at index 0
                    end=0     # Return to depot
                )
                problem_instance.add_vehicle(vehicle)
            
            # Add jobs
            debug_print("Step 6: Adding jobs", prefix="VROOM-STEP")
            for location in locations[1:]:  # Skip depot (index 0)
                # Handle coordinates whether they're a tuple or an object
                if isinstance(location.coordinates, tuple):
                    coord_tuple = location.coordinates
                else:
                    coord_tuple = (location.coordinates.latitude, location.coordinates.longitude)
                
                location_index = unique_coords[coord_tuple]
                job = vroom.Job(
                    id=location.id,  # Use the job ID from Excel
                    location=location_index  # Use the mapped location index
                )
                problem_instance.add_job(job)
            
            # Solve
            debug_print("Step 7: Solving optimization problem", prefix="VROOM-STEP")
            solution = problem_instance.solve(exploration_level=5, nb_threads=4)
            
            debug_print("Step 8: Processing solution", prefix="VROOM-STEP")
            debug_print(f"Solution type: {type(solution)}", prefix="VROOM-DEBUG")
            debug_print(f"Solution attributes: {dir(solution)}", prefix="VROOM-DEBUG")
            
            # Convert solution to routes
            debug_print("Step 9: Converting solution to routes", prefix="VROOM-STEP")
            optimized_routes = []
            
            if not hasattr(solution, 'routes'):
                raise ValueError(f"Unexpected solution format: {solution}")
            
            # Group routes by vehicle_id
            current_vehicle_id = None
            current_route_locations = []
            current_route_timing = {
                'total_duration': 0,
                'arrival_times': [],
                'service_times': [],
                'waiting_times': []
            }
            
            for _, row in solution.routes.iterrows():
                vehicle_id = row['vehicle_id']
                step_type = row['type']
                
                # If we've moved to a new vehicle, save the previous route
                if current_vehicle_id is not None and vehicle_id != current_vehicle_id:
                    # Add depot as ending location for previous route
                    current_route_locations.append(depot_location)
                    current_route_timing['arrival_times'].append(row['arrival'])
                    
                    optimized_route = Route(
                        vehicle_id=current_vehicle_id,
                        locations=current_route_locations.copy(),
                        total_distance=0.0,  # We'll need to calculate this if needed
                        total_time=float(current_route_timing['total_duration']),
                        sequence_numbers=list(range(len(current_route_locations)))
                    )
                    optimized_routes.append(optimized_route)
                    
                    # Reset for new vehicle
                    current_route_locations = []
                    current_route_timing = {
                        'total_duration': 0,
                        'arrival_times': [],
                        'service_times': [],
                        'waiting_times': []
                    }
                
                # Start processing new vehicle
                if current_vehicle_id != vehicle_id:
                    current_vehicle_id = vehicle_id
                    # Add depot as starting location
                    current_route_locations = [depot_location]
                    current_route_timing['arrival_times'].append(row['arrival'])
                    current_route_timing['service_times'].append(row['service'])
                    current_route_timing['waiting_times'].append(row['waiting_time'])
                
                # Add job location if this is a job step
                if step_type == 'job':
                    job_id = row['id']
                    location = next(loc for loc in locations if loc.id == job_id)
                    if isinstance(location.address, str):
                        # Convert string address to Address object if needed
                        location = Location(
                            id=location.id,
                            coordinates=location.coordinates,
                            address=Address(
                                postal_code="",  # You might want to extract this from the address string
                                street_name=location.address
                            )
                        )
                    current_route_locations.append(location)
                    current_route_timing['arrival_times'].append(row['arrival'])
                    current_route_timing['service_times'].append(row['service'])
                    current_route_timing['waiting_times'].append(row['waiting_time'])
                    current_route_timing['total_duration'] = row['duration']
            
            # Don't forget to add the last route
            if current_route_locations:
                # Add depot as ending location
                current_route_locations.append(depot_location)
                last_row = solution.routes.iloc[-1]
                current_route_timing['arrival_times'].append(last_row['arrival'])
                
                optimized_route = Route(
                    vehicle_id=current_vehicle_id,
                    locations=current_route_locations.copy(),
                    total_distance=0.0,  # We'll need to calculate this if needed
                    total_time=float(current_route_timing['total_duration']),
                    sequence_numbers=list(range(len(current_route_locations)))
                )
                optimized_routes.append(optimized_route)
            
            debug_print("Step 10: Optimization completed", prefix="VROOM-STEP")
            return optimized_routes
            
        except Exception as e:
            debug_print("Error details:", prefix="VROOM-ERROR")
            debug_print(f"Exception type: {type(e)}", prefix="VROOM-ERROR")
            debug_print(f"Exception message: {str(e)}", prefix="VROOM-ERROR")
            debug_print("Location details:", prefix="VROOM-ERROR")
            for loc in locations:
                coords = loc.coordinates if isinstance(loc.coordinates, tuple) else (loc.coordinates.latitude, loc.coordinates.longitude)
                debug_print(
                    f"ID={loc.id}, "
                    f"Coords={coords}, "
                    f"Address={loc.address.full_address}",
                    prefix="VROOM-ERROR"
                )
            raise