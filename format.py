import sys
import os
import json
import csv


args = sys.argv
directory = './jsons_premium'
output = './formatted.csv'
write_header = True
header = []

for index, path in enumerate(os.listdir(directory)):

    with open(directory + '/' + path, 'r') as f:
        data = json.load(f)

    row = []
    for key in data:
        if index == 0:
            header.append(key)
        row.append(data[key])

    if not os.path.isfile(output):
        with open(output, 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(header)
            writer.writerow(row)
    else:
        with open(output, 'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(row)

    print(f'Row {index} done!')
