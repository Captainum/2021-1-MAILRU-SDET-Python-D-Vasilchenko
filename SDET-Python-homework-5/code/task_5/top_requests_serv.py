import argparse
import json

parser = argparse.ArgumentParser(description='Подсчитывает топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой')
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
            status = request.strip().split(' ')[8][0:]
            ip = request.strip().split(' ')[0][0:]
            if status[0] == '5':
                if ip in requests:
                    requests[ip] += 1
                else:
                    requests[ip] = 1

top_requests = sorted(requests, key=requests.get, reverse=True)[0:5]

if json_flag:
    result = []
    for ip in top_requests:
        result.append(
            {
                'IP': ip,
                'COUNT': requests[ip]
            }
        )
    with open('result.json', 'w') as f:
        json.dump(result, f, indent = 4)
else:
    with open(outputfile, 'w') as f:
        f.write('Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой:')
        for ip in top_requests:
            f.write('\n\n')
            f.write(f'{ip}\n{requests[ip]}')