# Sam Heck, Student ID: 012082457

import os
import csv
from utils import format_address, parse_delivery_deadline
from package import Package, PackageStatus
from hash_table import HashTable
from truck import Truck
import datetime
from nearest_neighbor import nearest_neighbor

########## DATA IMPORT ##########

# Get file paths for data csv files
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DISTANCE_CSV_PATH = os.path.join(PROJECT_ROOT, 'data', 'distance_table.csv')
PACKAGE_FILE_PATH = os.path.join(PROJECT_ROOT, 'data', 'WGUPS_package_file.csv')

# open distance table csv file, parse and import data into in-memory distance_table_matrix and associated address_index_map. This will store all distance table data as a 2d array with a map for associating an address with a matching row/column index in the distance_table_matrix.
distance_table_matrix = []
address_index_map = {}
with open(DISTANCE_CSV_PATH, newline='') as distance_csvfile:
    distance_stream = csv.reader(distance_csvfile, delimiter=',', dialect='excel')
    for index, row in enumerate(distance_stream):
        address = row[0].split('\n')
        address_index_map[format_address(address[0], address[1])] = index

        distances = []
        for i in range(1, len(row)):
            distances.append(row[i])
        distance_table_matrix.append(distances)

# fill out empty side of matrix since distance is same regardless of direction and convert to floats
for i in range(0, len(distance_table_matrix)):
    for j in range(0, len(distance_table_matrix[i])):
        if distance_table_matrix[i][j] == '':
            distance_table_matrix[j][i] = float(distance_table_matrix[j][i]) #convert existing values to float before copying to other side of matrix
            distance_table_matrix[i][j] = distance_table_matrix[j][i]
        else:
            distance_table_matrix[i][j] = float(distance_table_matrix[i][j])

# open package csv file, parse and create package objects.
packages = HashTable()
with open(PACKAGE_FILE_PATH, newline='') as package_csvfile:
    package_stream = csv.reader(package_csvfile, delimiter=',', dialect='excel')
    for index, row in enumerate(package_stream):
        if index == 0: continue
        key = int(row[0])
        package = Package(package_id=key, street_address=row[1], city=row[2], state=row[3], zip_code=row[4], delivery_deadline=parse_delivery_deadline(row[5]), weight_kg=int(row[6]), special_notes=row[7])
        packages.insert(key, package)

########## PACKAGE-TRUCK ASSIGNMENT ##########

# The following section is hard coded package to truck assignment logic. Although this is ugly it was not in the requirements to implement a system to effectively distribute the packages to each truck. Attempting to implement that logic would require some business constraints to be added as fields in the package data excel file so that they could be properly sorted in code. This is a temporary work around to get the program working and could be improved later.

# This is the required package layout, everything else added after this can go on any truck and be delivered by EOD
# truck_1_ids = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]
# truck_2_ids = [3, 18, 36, 38] # These must be on truck 2
# truck_3_ids = [6, 9, 25, 28, 32,] # 6 and 25 must be delivered by 10:30 AM
# Truck 1 leaves at 8
# Truck 2 leaves when a driver returns
# Truck 3 leaves at 9:05 

current_time = datetime.time(8,0,0)
wrong_address_fixed_time = datetime.time(10, 20, 0)

truck_configs = [
    (1, [15, 1, 13, 14, 16, 20, 29, 30, 31, 34, 37, 40, 19, 33, 27], datetime.time(8, 0, 0)), # (13 required) (15)
    (2, [3, 9, 18, 36, 38, 2, 4, 5, 7, 8, 10, 11, 12, 17, 35, 39], None), # (5 required) (16)
    (3, [6, 25, 28, 32, 21, 22, 23, 24, 26], datetime.time(9, 5, 0)) # (5 required) (9)
]

# instantiate the 3 trucks and load package lists, set known departure times
trucks: list[Truck] = []
for truck_id, id_list, departure_time in truck_configs:
    package_list = []
    for id in id_list:
        package_list.append(packages.get(id))
    trucks.append(Truck(id=truck_id, packages=package_list, departure_time=departure_time))

# build routes for truck 1 and 3. truck 2 needs route recalculated after address is changed a 10:20 and departure time is set.
for i, truck in enumerate(trucks):
    if truck.get_departure_time() != None:
        truck.build_route(distance_table_matrix, address_index_map)
        truck.calc_delivery_times()

# calculate truck 2's departure time to either the larger of the two: time the earliest truck returns or time the wrong address is fixed.
time_earliest_truck_returns = min(trucks[0].get_return_time(), trucks[2].get_return_time())
trucks[1].set_departure_time(max(time_earliest_truck_returns, wrong_address_fixed_time))

########## USER INPUT ##########
user_requested_time = input("Please input a time in the following format: <hour>:<minute>:<seconds>\n").split(":")
current_time = datetime.time(hour=int(user_requested_time[0]), minute=int(user_requested_time[1]), second=int(user_requested_time[2]))

# Update package with wrong address if time is after 10:20. recalculate truck 2's route.
if current_time >= wrong_address_fixed_time:
    packages.get(9).set_address(street_address='410 S State St', city='Salt Lake City', state='UT', zip_code='84111')
    trucks[1].build_route(distance_table_matrix, address_index_map)
    trucks[1].calc_delivery_times()

# update status's of all packages. 
# Loop through each trucks and if current time is greater than departure time, enter a loop into the route list. at each route_stop check if delivery time is greater than current time, if so set package status to deliverd, if not set to 'en route'
for truck in trucks:
    if truck.get_departure_time() <= current_time:
        for package in truck.get_package_list():
            if package.get_delivery_time() != None and package.get_delivery_time() <= current_time:
                package.set_status(PackageStatus.DELIVERED)
            else: package.set_status(PackageStatus.EN_ROUTE)

########### PRINTING RESULTS ###########

def print_route_summary(trucks: list[Truck]):
    packages_overdue = 0
    total_distance = 0
    for i, truck in enumerate(trucks):
        total_distance += truck.get_route().get_total_distance()
        print(f"Truck {truck.id}:\troute_distance: {truck.get_route().get_total_distance()}\tdeparture time: {truck.departure_time}\treturn time: {truck.return_time}")
        # Print packages in route order if route is completed, else in import order into the truck's package_list field.
        if truck.get_route_length() > 0:
            for route_stop in truck.get_route():
                if route_stop.package.delivery_time != None and route_stop.package.delivery_time > route_stop.package.delivery_deadline:
                    packages_overdue += 1
                    print(f"Package late on truck {truck.id}\nPackage: {package}")  
                print(route_stop.package)
        else:
            for package in truck.get_package_list():
                if package.delivery_time != None and package.delivery_time > package.delivery_deadline:
                    packages_overdue += 1
                    print(f"Package late on truck {truck.id}\nPackage: {package}")  
                print(package)
    print(f"Total Distance: {total_distance} miles")
    print(f"Packages Overdue: {packages_overdue}")

print_route_summary(trucks)