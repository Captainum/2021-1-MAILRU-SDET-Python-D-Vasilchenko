import argparse
import json

parser = argparse.ArgumentParser(description='Подсчитывает общее количество запросов')
parser.add_argument('-i', '--ifile', dest='inputfile', required=True, help='путь к .log файлу')
parser.add_argument('-o', '--ofile', dest='outputfile', required=True, help='путь к файлу с отчетом')
parser.add_argument('--json', dest='json_flag', action='store_true', help='сохраняет отчет в JSON формате')

args = parser.parse_args()

inputfile = args.inputfile
outputfile = args.outputfile
json_flag = args.json_flag

count = 0

with open(inputfile, 'r') as f:
    while True:
        request = f.readline()
        if not request:
            break
        else:
            count += 1

if json_flag:
    result = {"TOTAL COUNT": count}
    with open('result.json', 'w') as f:
        json.dump(result, f, indent = 4)
else:
    with open(outputfile, 'w') as f:
        f.write(f'Общее количество запросов:\n{count}')