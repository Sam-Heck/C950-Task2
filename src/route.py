from package import Package
from typing import Iterator

class RouteStop:
    def __init__(self, package: Package, distance_from_last_stop):
        self.package = package
        self.distance_from_last_stop = distance_from_last_stop

class Route:
    def __init__(self, route: list[RouteStop] = None):
        self.route = route if route is not None else []
        self.total_distance = 0.0
        self.return_to_hub_distance = 0.0

    def add_route_stop(self, package, distance_from_last_stop):
        route_stop = RouteStop(package=package, distance_from_last_stop=distance_from_last_stop)
        self.route.append(route_stop)

    def add_to_total_distance(self, distance):
        self.total_distance += distance

    def get_route(self) -> list[RouteStop]:
        return self.route
    
    def get_length(self):
        return len(self.route)
    
    def get_total_distance(self):
        return self.total_distance
    
    def set_return_to_hub_distance(self, distance):
        self.return_to_hub_distance = distance

    def __iter__(self) -> Iterator[RouteStop]:
        return iter(self.route)