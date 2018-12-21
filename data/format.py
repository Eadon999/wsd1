import sys
import os
import json
import csv


def split_dictionary(dictionaries):
    ingredients = [dictionary[key]
                   for dictionary in dictionaries for key in dictionary if key == 'name']
    amount = [dictionary[key]
              for dictionary in dictionaries for key in dictionary if key == 'quantity']

    return ingredients, amount


if __name__ == '__main__':
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
            if key == 'recipeIngredient':
                ingredients, amount = split_dictionary(data[key])
                concat_ingredients = [ingredients, amount]
                row.append(concat_ingredients)
            else:
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
