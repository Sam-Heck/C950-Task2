import os
import csv
from utils import format_address

# Get file paths for data csv files
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DISTANCE_CSV_PATH = os.path.join(PROJECT_ROOT, 'data', 'distance_table.csv')


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

# fill out other side of matrix since distance is same regardless of direction.
for i in range(0, len(distance_table_matrix)):
    for j in range(0, len(distance_table_matrix[i])):
        if distance_table_matrix[i][j] == '':
            distance_table_matrix[i][j] = distance_table_matrix[j][i]
