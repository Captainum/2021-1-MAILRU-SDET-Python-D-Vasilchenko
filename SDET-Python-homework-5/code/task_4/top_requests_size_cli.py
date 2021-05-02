import argparse
import json

parser = argparse.ArgumentParser(description='Подсчитывает топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой')
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
            url = request.strip().split(' ')[6][0:]
            status = request.strip().split(' ')[8][0:]
            size = request.strip().split(' ')[9][0:]
            if size != '-':
                size = int(size)
            ip = request.strip().split(' ')[0][0:]
            data = (url, status, ip)
            if status[0] == '4':
                if data in requests:
                    if size > requests[data]:
                        requests[data] = size
                else:
                    requests[data] = size

top_requests = sorted(requests, key=requests.get, reverse=True)[0:5]

if json_flag:
    result = []
    for request in top_requests:
        result.append(
            {
                'URL': request[0],
                'STATUS': request[1],
                'SIZE': requests[request],
                'IP': request[2]
            }
        )
    with open('result.json', 'w') as f:
        json.dump(result, f, indent = 4)
else:
    with open(outputfile, 'w') as f:
        f.write('Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой:')
        for request in top_requests:
            f.write('\n\n')
            f.write(f'{request[0]}\n{request[1]}\n{requests[request]}\n{request[2]}')