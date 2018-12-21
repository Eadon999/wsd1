import sys
import os
import json
import csv


args = sys.argv
directory = './jsons_premium'
write_header = True
header = []


def split_dictionary(dictionaries):
    ingredients = [dictionary[key]
                   for dictionary in dictionaries for key in dictionary if key == 'name']
    amount = [dictionary[key]
              for dictionary in dictionaries for key in dictionary if key == 'quantity']

    return ingredients, amount


if __name__ == '__main__':
    for index, path in enumerate(os.listdir(directory)):
        with open(directory + '/' + path, 'r') as f:
            data = json.load(f)

        for key in data:
            output = f'./{key}_output.csv'
            row = []
            if index == 0:
                header = [key]

            if key == 'recipeIngredient':
                ingredients, amount = split_dictionary(data[key])
                row.append(ingredients)
                row.append(amount)
            elif data[key] is not None:
                row.append(data[key])
            else:
                row.append('N/A')

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
