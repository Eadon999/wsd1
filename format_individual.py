import sys
import os
import json
import csv


args = sys.argv
directory = './jsons_premium'
write_header = True
header = []

for index, path in enumerate(os.listdir(directory)):

    with open(directory + '/' + path, 'r') as f:
        data = json.load(f)

    for key in data:
        output = f'./{key}_output.csv'
        input = []
        if index == 0:
            header = [key]

        if data[key] is not None:
            input.append(data[key])
        else:
            input.append('N/A')

        if not os.path.isfile(output):
            with open(output, 'w') as f:
                writer = csv.writer(f, lineterminator='\n')
                writer.writerow(header)
                writer.writerow(input)
        else:
            with open(output, 'a') as f:
                writer = csv.writer(f, lineterminator='\n')
                writer.writerow(input)

    print(f'Row {index} done!')
