# Sam Heck, Student ID: 012082457

import os
import csv
from utils import format_address, parse_delivery_deadline
from package import Package
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
# Truck ideas:
#   Truck 1 takes all 12 urgent deadline packages plus 1 other required package and leaves at 8:00 AM (13)
#   Truck 3 takes the 2 remaining urgent packages that were delayed on flight plus the rest of the delay flight packages plus 8 more packages and leaves at 9:05 AM (13)
#   Truck 2 takes its 4 required packages plus 10 more and leaves after either truck 1 or truck 2 driver gets back.

# This is the required package layout, everything else added after this can go on any truck and be delivered by EOD
# truck_1_ids = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]
# truck_2_ids = [3, 18, 36, 38] # These must be on truck 2
# truck_3_ids = [6, 9, 25, 28, 32,] # 6 and 25 must be delivered by 10:30 AM
# Truck 1 leaves at 8
# Truck 2 leaves when a driver returns
# Truck 3 leaves at 9:05 

# Potential grouping: 
# truck_configs = [
#     (1, [[15], [1, 13, 14, 16, 20, 29, 30, 31, 34, 37, 40], [19]], datetime.time(8, 0, 0)), # (13)
#     (2, [3, 9, 18, 36, 38, 2, 4, 5, 7, 8, 10, 11, 12, 17], None), # (5 required) (Take 10 more flexible ones) (15)
#     (3, [[6, 25], 28, 32, 21, 22, 23, 24, 26, 27, 33, 35, 39], datetime.time(9, 5, 0)) # (5 required) (Take 7 more flexible ones) (13)
# ]

truck_configs = [
    (1, [15, 1, 13, 14, 16, 20, 29, 30, 31, 34, 37, 40, 19], datetime.time(8, 0, 0)), # (13)
    (2, [3, 9, 18, 36, 38, 2, 4, 5, 7, 8, 10, 11, 12, 17], None), # (5 required) (Take 9 more flexible ones) (14)
    (3, [6, 25, 28, 32, 21, 22, 23, 24, 26, 27, 33, 35, 39], datetime.time(9, 5, 0)) # (5 required) (Take 7 more flexible ones) (13)
]

# instantiate the 3 trucks and load package lists, set known departure times
trucks: list[Truck] = []
for truck_id, id_list, departure_time in truck_configs:
    package_list = []
    for id in id_list:
        package_list.append(packages.get(id))
    trucks.append(Truck(id=truck_id, packages=package_list, departure_time=departure_time))

# build routes 
for i, truck in enumerate(trucks):
    truck.set_route(nearest_neighbor(truck.get_package_list(), distance_table_matrix, address_index_map))
    if truck.departure_time != None:
        truck.calc_delivery_times()
    # print(truck)
    for package in truck.get_package_list():
        if package.delivery_time != None and package.delivery_time > package.delivery_deadline:
            print(f"Package late on truck {truck.id}\nPackage: {package}")
# find whichever truck returns first and set that time to truck 2's departure time, if it's less than 10:20 set truck 2's departure time to 10:20. then call calc deliver times on truck 2. Status updates will occur in the cli interface when checking the status of packages

# Build truck 2's route after one of the other trucks gets back and time is after 10:20 to ensure the wrong address for package 9 is updated. Also routes will likely need a start time to be built.