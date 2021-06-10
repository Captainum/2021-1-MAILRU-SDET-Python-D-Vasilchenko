import os

def total_requests(log_root):
    count = 0

    with open(os.path.join(log_root, 'access.log'), 'r') as f:
        while True:
            request = f.readline()
            if not request:
                break
            else:
                count += 1
    result = {'TOTAL COUNT': count}

    return result


def total_requests_type(log_root):
    requests = {}

    with open(os.path.join(log_root, 'access.log'), 'r') as f:
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

    result = []
    for method in top_methods:
        result.append(
            {
                "METHOD": method,
                "COUNT": requests[method]
            }
        )
    
    return result


def top_requests_url(log_root):
    urls = {}

    with open(os.path.join(log_root, 'access.log'), 'r') as f:
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

    result = []
    for url in top_url:
        result.append(
            {
                'URL': url,
                'COUNT': urls[url]
            }
        )

    return result


def top_requests_size_cli(log_root):
    requests = {}

    with open(os.path.join(log_root, 'access.log'), 'r') as f:
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

    return result


def top_requests_serv(log_root):
    requests = {}

    with open(os.path.join(log_root, 'access.log'), 'r') as f:
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

    result = []
    for ip in top_requests:
        result.append(
            {
                'IP': ip,
                'COUNT': requests[ip]
            }
        )

    return result