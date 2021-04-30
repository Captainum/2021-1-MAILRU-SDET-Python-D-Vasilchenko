import argparse
import json

parser = argparse.ArgumentParser(description='Подсчитывает топ 10 самых частых запросов')
parser.add_argument('-i', '--ifile', dest='inputfile', required=True, help='путь к .log файлу')
parser.add_argument('-o', '--ofile', dest='outputfile', required=True, help='путь к файлу с отчетом')
parser.add_argument('--json', dest='json_flag', action='store_true', help='сохраняет отчет в JSON формате')

args = parser.parse_args()

inputfile = args.inputfile
outputfile = args.outputfile
json_flag = args.json_flag

urls = {}

with open(inputfile, 'r') as f:
    while True:
        request = f.readline()
        if not request:
            break
        else:
            t = request.strip().split(' ')[6][0:]
            if t in urls:
                urls[t] += 1
            else:
                urls[t] = 1
            
top_url = sorted(urls, key=urls.get, reverse=True)[0:10]

if json_flag:
    result = []
    for url in top_url:
        result.append(
            {
                'URL': url,
                'COUNT': urls[url]
            }
        )
    
    with open('result.json', 'w') as f:
        json.dump(result, f, indent = 4)
else:
    with open(outputfile, 'w') as f:
        f.write('Топ 10 самых частых запросов:')
        for url in top_url:
            f.write('\n\n')
            f.write(f'{url}\n{urls[url]}')