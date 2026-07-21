from package import Package
from utils import add_time
from route import RouteStop, Route
from nearest_neighbor import nearest_neighbor

class Truck:
    speed = 18
    def __init__(self, id, packages: list[Package], departure_time = None):
        self.id = id
        self.packages = packages
        self.route: Route = Route()
        self.departure_time = departure_time
        self.return_time = None

    def get_package_list(self):
        return self.packages

    def add_package(self, package: Package):
        self.packages.append(package)

    def get_departure_time(self):
        return self.departure_time

    def set_departure_time(self, time):
        self.departure_time = time

    def get_return_time(self):
        return self.return_time

    def set_return_time(self, time):
        self.return_time = time

    def get_route(self):
        return self.route
    
    def get_route_length(self):
        return self.route.get_length()

    def set_route(self, route):
        self.route = route

    def build_route(self, distance_table, address_map):
        self.set_route(nearest_neighbor(self.get_package_list(), distance_table, address_map))

    def calc_delivery_times(self):
            # loop through route list, at each loop calculate and set delivery time for that package. At each loop we will be on a RouteStop object which has the distance from last stop and so we will need to keep a running time that updates each loop. after we know the time it takes
            current_time = self.departure_time
            for route_stop in self.route:
                duration_hours = route_stop.distance_from_last_stop / Truck.speed
                delivery_time = add_time(current_time, hours=duration_hours)
                route_stop.package.delivery_time = delivery_time
                current_time = delivery_time
            self.return_time = add_time(self.departure_time, hours=self.route.get_total_distance() / Truck.speed)

    def __str__(self):
        return (
            f"Truck ID: {self.id}\n"
            f"Package list Qty: {len(self.packages)}\n"
            f"Route Stops Qty: {self.get_route_length()}\n"
            f"Departure Time: {self.departure_time}\n"
            f"Return Time: {self.return_time}\n"
            f"Total Distance: {self.route.get_total_distance()}"
        )
                
