import vroom
from typing import List, Dict
from domain.travelling_salesman.entities.location import Location

class JobService:
    def add_jobs(self, problem_instance: vroom.Input, locations: List[Location], unique_coords: Dict):
        print("*" * 50)

        for location in locations[0:]:
            location_index = unique_coords[(location.coordinates.latitude, location.coordinates.longitude)]
            job = vroom.Job(id=location.id, location=location_index)
            print(location.id, location_index)
            problem_instance.add_job(job) 