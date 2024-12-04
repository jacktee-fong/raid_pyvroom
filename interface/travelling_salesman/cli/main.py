import argparse
import os
from dotenv import load_dotenv
from infrastructure.travelling_salesman.repositories.excel_location_repository import ExcelLocationRepository
from infrastructure.travelling_salesman.services.vroom_optimizer_service import VroomOptimizerService
from infrastructure.travelling_salesman.services.onemap_service import OneMapService
from application.travelling_salesman.use_cases.load_locations_use_case import LoadLocationsUseCase
from application.travelling_salesman.use_cases.get_optimal_routes_use_case import GetOptimalRoutesUseCase
from application.travelling_salesman.services.route_planning_service import RoutePlanningService
from interface.travelling_salesman.dto.location_dto import LocationDTO
from interface.travelling_salesman.dto.route_dto import RouteDTO

# Load environment variables
load_dotenv()


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Traveling Salesman Problem Solver")
    
    parser.add_argument(
        "--file_path", 
        type=str, 
        default="store/data/travelling_salesman.xlsx",
        help="Path to the Excel file containing locations"
    )
    parser.add_argument(
        "--max_vehicles", 
        type=int, 
        default=1, 
        help="Maximum number of vehicles to use"
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
    
    # Check DEBUG environment variable
    debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'
    
    if debug_mode:
        # Return default debug values
        return parser.parse_args([])
    
    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    print(f"Processing file: {args.file_path}")
    print(f"Maximum vehicles: {args.max_vehicles}")
    print(f"Output file: {args.output_file}")
    
    # Initialize repository and services
    location_repository = ExcelLocationRepository(args.file_path)
    route_optimizer = VroomOptimizerService()
    onemap_service = OneMapService()
    
    # Initialize use cases
    load_locations_use_case = LoadLocationsUseCase(location_repository)
    get_optimal_routes_use_case = GetOptimalRoutesUseCase(route_optimizer)
    
    # Initialize service orchestrator
    route_planning_service = RoutePlanningService(
        load_locations_use_case,
        get_optimal_routes_use_case
    )
    
    # Plan routes
    routes = route_planning_service.plan_routes(
        max_vehicles=args.max_vehicles,
        matrix_type=args.matrix_type
    )
    
    # Display results
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
    
    # Plot routes on map
    routes_for_plotting = []
    for route in routes:
        routes_for_plotting.append(route.locations)
    
    # Plot all routes at once
    onemap_service.plot_routes(routes_for_plotting, args.output_file)

    print(f"\nRoute map has been generated: {args.output_file}")


if __name__ == "__main__":
    args = get_args()
    main(args)
