# Sam Heck, Student ID: 012082457

import os
import csv
from utils import format_address, parse_delivery_deadline
from Package import Package
from Hash_Table import Hash_Table

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

# fill out empty side of matrix since distance is same regardless of direction.
for i in range(0, len(distance_table_matrix)):
    for j in range(0, len(distance_table_matrix[i])):
        if distance_table_matrix[i][j] == '':
            distance_table_matrix[i][j] = distance_table_matrix[j][i]

# open package csv file, parse and create package objects.
packages = Hash_Table()
with open(PACKAGE_FILE_PATH, newline='') as package_csvfile:
    package_stream = csv.reader(package_csvfile, delimiter=',', dialect='excel')
    for index, row in enumerate(package_stream):
        if index == 0: continue
        key = int(row[0])
        package = Package(package_id=key, street_address=row[1], city=row[2], state=row[3], zip_code=int(row[4]), delivery_deadline=parse_delivery_deadline(row[5]), weight_kg=int(row[6]), special_notes=row[7])
        packages.insert(key, package)