from package import Package

class Truck:
    speed = 18
    def __init__(self, id, packages: list[Package], departure_time = None):
        self.id = id
        self.packages = packages
        self.route = None
        self.departure_time = departure_time
        self.return_time = None

    def get_package_list(self):
        return self.packages

    def add_package(self, package: Package):
        self.packages.append(package)

    def set_departure_time(self, time):
        self.departure_time = time

    def set_return_time(self, time):
        self.return_time = time

    def set_route(self, route):
        self.route = route