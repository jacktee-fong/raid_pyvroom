import argparse
import os
from dotenv import load_dotenv
from infrastructure.travelling_salesman.repositories.excel_location_repository import ExcelLocationRepository
from infrastructure.travelling_salesman.services.vroom_optimizer_service import VroomOptimizerService
from infrastructure.onemap_service import OneMapService
from infrastructure.matrix_service import MatrixService
from infrastructure.vehicle_service import VehicleService
from infrastructure.job_service import JobService
from infrastructure.solution_processor_service import SolutionProcessorService
from application.travelling_salesman.use_cases.load_locations_use_case import LoadLocationsUseCase
from application.travelling_salesman.use_cases.get_optimal_routes_use_case import GetOptimalRoutesUseCase
from application.travelling_salesman.services.route_planning_service import RoutePlanningService
from interface.travelling_salesman.dto.location_dto import LocationDTO
from interface.travelling_salesman.dto.route_dto import RouteDTO
from domain.travelling_salesman.entities.location import Location
from domain.travelling_salesman.value_objects.address import Address
from domain.travelling_salesman.value_objects.coordinates import Coordinates

# Load environment variables
load_dotenv()


def get_args(debug: bool = False) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Traveling Salesman Problem Solver")
    
    parser.add_argument(
        "--file_path", 
        type=str, 
        default="store/data/travelling_salesman.xlsx",
        help="Path to the Excel file containing locations"
    )
    parser.add_argument(
        "--num_vehicles", 
        type=int, 
        default=6,  # Set default value
        help="Number of vehicles to use"
    )
    parser.add_argument(
        "--output_file", 
        type=str, 
        default="route_map.html", 
        help="Path to the output HTML file"
    )
    parser.add_argument(
        "--matrix_type",
        type=str,
        choices=["duration", "distance"],
        default="duration",
        help="Type of matrix to use for optimization"
    )
    
    if debug:
        # Return default debug values
        return parser.parse_args([])
    
    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    print(f"Processing file: {args.file_path}")
    print(f"Number of vehicles: {args.num_vehicles}")
    print(f"Output file: {args.output_file}")
    
    # Initialize repository and services
    location_repository = ExcelLocationRepository(args.file_path)
    onemap_service = OneMapService()
    matrix_service = MatrixService(onemap_service)
    vehicle_service = VehicleService()
    job_service = JobService()
    solution_processor_service = SolutionProcessorService()
    
    # Set default depot location
    depot_coords = onemap_service.get_coordinates("338729")
    if not depot_coords:
        raise ValueError("Could not get coordinates for depot postal code 338729")
        
    depot_location = Location(
        id=0,  # Use 0 for depot
        coordinates=depot_coords,  # Already a Coordinates object
        address=Address(
            postal_code="338729",
            full_address="Default Depot (338729)",
        )
    )
    
    # Initialize optimizer with services
    route_optimizer = VroomOptimizerService(
        matrix_service,
        vehicle_service,
        job_service,
        solution_processor_service
    )
    
    # Initialize use cases
    load_locations_use_case = LoadLocationsUseCase(location_repository)
    get_optimal_routes_use_case = GetOptimalRoutesUseCase(route_optimizer)
    
    # Initialize service orchestrator
    route_planning_service = RoutePlanningService(
        load_locations_use_case,
        get_optimal_routes_use_case
    )
    
    # Plan routes
    routes, unassigned = route_planning_service.plan_routes(
        max_vehicles=args.num_vehicles,
        matrix_type=args.matrix_type,
        depot_location=depot_location  # Pass depot location
    )
    
    # Display results for assigned routes
    print("\nAssigned Routes:")
    for route in routes:
        route_dto = RouteDTO(
            vehicle_id=route.vehicle_id,
            locations=[LocationDTO(loc.id, loc.address.postal_code, loc.address.full_address) for loc in route.locations],
            total_distance=route.total_distance,
            total_time=route.total_time
        )
        print(f"\nVehicle {route_dto.vehicle_id}:")
        for loc in route_dto.locations:
            print(f"  - {loc.address} (Postal Code: {loc.postal_code})")
        print(f"Total Distance: {route_dto.total_distance} meters")
        print(f"Total Time: {route_dto.total_time} seconds")
    
    # Display unassigned locations
    print("\nUnassigned Locations:")
    for location in unassigned:
        location_dto = LocationDTO(
            location.id,
            location.address.postal_code,
            location.address.full_address
        )
        print(f"  - {location_dto.address} (Postal Code: {location_dto.postal_code})")
    
    # Plot routes on map
    routes_for_plotting = []
    for route in routes:
        routes_for_plotting.append(route.locations)
    
    # Plot all routes at once
    onemap_service.plot_routes(routes_for_plotting, args.output_file)
    
    print(f"\nRoute map has been generated: {args.output_file}")


if __name__ == "__main__":
    args = get_args(debug=True)
    # Override specific arguments for testing
    args.num_vehicles = 6  # Set custom number of vehicles
    args.matrix_type = "duration"  # Set custom matrix type
    args.output_file = "route_map.html"  # Set custom output file
    args.file_path = "store/data/travelling_salesman.xlsx"  # Set custom input file
    main(args)
