import argparse
import json

parser = argparse.ArgumentParser(description='Подсчитывает общее количество запросов по типу')
parser.add_argument('-i', '--ifile', dest='inputfile', required=True, help='путь к .log файлу')
parser.add_argument('-o', '--ofile', dest='outputfile', required=True, help='путь к файлу с отчетом')
parser.add_argument('--json', dest='json_flag', action='store_true', help='сохраняет отчет в JSON формате')

args = parser.parse_args()

inputfile = args.inputfile
outputfile = args.outputfile
json_flag = args.json_flag

requests = {}

with open(inputfile, 'r') as f:
    while True:
        request = f.readline()
        if not request:
            break
        else:
            t = request.strip().split(' ')[5][1:]
            if t in requests:
                requests[t] += 1
            else:
                requests[t] = 1

top_methods = sorted(requests, key=requests.get, reverse=True)

if json_flag:
    result = []
    for method in top_methods:
        result.append(
            {
                "METHOD": method,
                "COUNT": requests[method]
            }
        )
    with open('result.json', 'w') as f:
        json.dump(result, f, indent = 4)
else:
    with open(outputfile, 'w') as f:
        f.write('Общее количество запросов по типу:')
        for method in top_methods:
            f.write('\n')
            f.write(f'{method} - {requests[method]}')