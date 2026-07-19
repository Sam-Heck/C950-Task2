from route import Route
from package import Package

def nearest_neighbor(package_list: list[Package], distance_table, address_index_map):
    route = Route()
    unvisited = list(package_list)
    hub_address = "4001 South 700 East|84107"
    current_address = hub_address

    # loop the length of unvisited. inside each loop, find the next closest package and save it to a variable.
    while len(unvisited) > 0:
        smallest_distance = float("inf")
        closest_package = unvisited[0]
        closest_package_index = 0
        for i, package in enumerate(unvisited):
            address = package.get_formatted_address()
            distance = distance_table[address_index_map[current_address]][address_index_map[address]]
            if distance < smallest_distance: 
                smallest_distance = distance
                closest_package = unvisited[i]
                closest_package_index = i
        
        current_address = closest_package.get_formatted_address()
        # add a routestop to the route list
        route.add_route_stop(package=closest_package, distance_from_last_stop=smallest_distance)
        route.add_to_total_distance(smallest_distance)
        # remove the current location (which is currently closest package from unvisited)
        unvisited.pop(closest_package_index)

    # after route is fully built, truck must return to hub. add one more route stop to return to hub.
    # calculate distance from current location to hub and set the field on route
    return_distance = distance_table[address_index_map[current_address]][address_index_map[hub_address]]
    route.set_return_to_hub_distance(return_distance)
    route.add_to_total_distance(return_distance)

    return route