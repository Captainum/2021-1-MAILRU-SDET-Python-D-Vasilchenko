from socket import socket

from flask import json

import logging

from datetime import datetime

from client.response_handler import ResponseHandler

class ClientSocket:
    
    def __init__(self, family=-1, type=-1, timeout=0.1):
        self.logger = logging.getLogger('client_logger')

        self.response_handler = ResponseHandler
        
        self.sock = socket(family, type)
        self.sock.settimeout(timeout)
    
    def _request(self, url, method, location, data=None, content_type='application/json'):
        
        url = url.split('/')[-1]

        host = url.split(':')[0]
        port = int(url.split(':')[1])

        self.sock.connect((host, port))
        
        request = None
        
        if data is None:
            request = f'{method} {location} HTTP/1.1\r\n' \
                      f'Host: {host}\r\n\r\n'
        else:
            if content_type == 'application/json':
                data = json.dumps(data)
            request = f'{method} {location} HTTP/1.1\r\n' \
                      f'Host: {host}\r\n' \
                      f'Content-Type: {content_type}\r\n' \
                      f'Content-Length: {len(data)}\r\n\r\n' \
                      f'{data}\r\n'

        self.logger.info('#' * 30)
        self.logger.info(f'timestamp: {datetime.now()}')
        self.logger.info('REQUEST:')
        self.logger.info(request)

        self.sock.send(request.encode())

        total_data = []

        while True:
            data = self.sock.recv(4096)
            if data:
                total_data.append(data.decode())
            else:
                self.sock.close()
                break
        response = ''.join(total_data)

        self.logger.info('RESPONSE:')
        self.logger.info(response)
        self.logger.info('#' * 30 + '\n')

        return self.response_handler.handle(response.splitlines())

    def get(self, url='127.0.0.1:80', location='/'):
        return self._request(url, 'GET', location)
    
    def post(self, url='127.0.0.1:80', location='/', data=None, content_type='application/json'):
        return self._request(url, 'POST', location, data)

    def put(self, url='127.0.0.1:80', location='/', data=None, content_type='application/json'):
        return self._request(url, 'PUT', location, data)
    
    def delete(self, url='127.0.0.1', location='/'):
        return self._request(url, 'DELETE', location)