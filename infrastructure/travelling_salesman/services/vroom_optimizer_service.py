from typing import List, Optional, Literal
import vroom
from domain.travelling_salesman.entities.location import Location
from application.travelling_salesman.interfaces.route_optimizer_interface import RouteOptimizerInterface, OptimizedRoute
from infrastructure.matrix_service import MatrixService
from infrastructure.vehicle_service import VehicleService
from infrastructure.job_service import JobService
from infrastructure.onemap_service import OneMapService
from infrastructure.solution_processor_service import SolutionProcessorService
# Initialize services
onemap_service = OneMapService()
matrix_service = MatrixService(onemap_service)
vehicle_service = VehicleService()
job_service = JobService()
solution_processor_service = SolutionProcessorService()

class VroomOptimizerService(RouteOptimizerInterface):
    def __init__(self, matrix_service: MatrixService, vehicle_service: VehicleService, 
                 job_service: JobService, solution_processor_service: SolutionProcessorService):
        self.matrix_service = matrix_service
        self.vehicle_service = vehicle_service
        self.job_service = job_service
        self.solution_processor_service = solution_processor_service

    def optimize_routes(self, locations: List[Location], max_vehicles: Optional[int] = None, 
                       depot_location: Optional[Location] = None, 
                       matrix_type: Literal["duration", "distance"] = "duration") -> List[OptimizedRoute]:
        try:
            # Step 1: Get matrices
            duration_matrix, distance_matrix = self.matrix_service.get_matrices(locations, matrix_type)

            # Step 2: Initialize VROOM problem
            problem_instance = vroom.Input()

            # Step 3: Set matrix
            if matrix_type == "duration":
                problem_instance.set_durations_matrix(profile="car", matrix_input=duration_matrix.tolist())
            else:
                problem_instance.set_durations_matrix(profile="car", matrix_input=distance_matrix.tolist())

            # Step 4: Add vehicles
            self.vehicle_service.add_vehicles(problem_instance, max_vehicles)

            # Step 5: Add jobs
            unique_coords = {(loc.coordinates.latitude, loc.coordinates.longitude): idx 
                            for idx, loc in enumerate(locations)}
            self.job_service.add_jobs(problem_instance, locations, unique_coords)

            # Step 6: Solve and process solution
            solution = problem_instance.solve(exploration_level=5, nb_threads=4)
            return self.solution_processor_service.process_solution(solution, locations, depot_location)

        except Exception as e:
            # Handle exceptions
            raise

# Initialize VroomOptimizerService with new services
route_optimizer = VroomOptimizerService(matrix_service, vehicle_service, job_service, solution_processor_service)

