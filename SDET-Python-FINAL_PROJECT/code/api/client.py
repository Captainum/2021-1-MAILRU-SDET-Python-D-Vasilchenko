import requests
from urllib.parse import urljoin
import json

import allure
import logging

from builder.builder import Builder


logger = logging.getLogger('test')


class ResponseStatusCodeException(Exception):
    pass


class HttpClient:

    def __init__(self, host, port):
        self.session = requests.Session()
        self.base_url = f'http://{host}:{port}'
        
        self.admin_cookie = None

        logger.debug('HttpClient initialized')
        
    @allure.step('make request: {method} {location}')
    def _request(self, method, location, headers=None, data=None, expected_status=200, jsonify=True, allow_redirects=True, cookies=None, files=None):
        url = urljoin(self.base_url, location)

        if cookies == None:
            cookies = self.admin_cookie
        response = self.session.request(method, url, headers=headers, data=data, allow_redirects=allow_redirects,files=files, cookies=cookies)
        
        logger.info(f'REQUEST: {method} {url}{location}\nHEADERS:{headers}\nDATA:{data}')
        logger.info(f'RESPONSE: {response.status_code}\nHEADERS:{response.headers}\nDATA:{response.content}')

        # if response.status_code != expected_status:
        #     raise ResponseStatusCodeException(f'Got {response.status_code} {response.reason} for URL "{url}"!\n'
        #                                       f'Expected status_code: {expected_status}.')

        if jsonify:
            json_response = response.json()
            return json_response
        return response


class ApiClient(HttpClient):

    @allure.step('ApiClient: create admin')
    def create_admin(self):
        location = '/reg'

        username, password, email = Builder.random_person()

        logger.info(f'ApiClient: create admin with username={username}, password={password}, email={email}')

        data = {}
        data['username'] = username
        # data['username'] = 'ADMINETOYA'
        data['email'] = email
        data['password'] = password
        data['confirm'] = password
        data['submit'] = 'Register'
        data['term'] = 'y'

        response = self._request('POST', location=location, data=data, jsonify=False)
        
        assert response.status_code == 200

        return self.session.cookies

    @allure.step('ApiClient: add user with username={username}, password={password}, email={email}')
    def post_add_user(self, username, password, email):
        
        logger.info(f'ApiClient: add user with username={username}, password={password}, email={email}')

        location = '/api/add_user'

        data = {}
        data['username'] = username
        data['password'] = password
        data['email'] = email

        response = self._request('POST', location=location, data=json.dumps(data), jsonify=False)

        return response

    @allure.step('ApiClient: delete user with username={username}')
    def get_del_user(self, username):
        logger.info(f'ApiClient: delete user with username={username}')

        location = f'/api/del_user/{username}'

        response = self._request('GET', location=location, jsonify=False)

        return response

    @allure.step('ApiClient: block user with username={username}')
    def get_block_user(self, username):
        logger.info(f'ApiClient: block user with username={username}')

        location = f'/api/block_user/{username}'

        response = self._request('GET', location=location, jsonify=False)

        return response

    @allure.step('ApiClient: accept user with username={username}')
    def get_accept_user(self, username):
        logger.info(f'accept user with username={username}')
        
        location = f'/api/accept_user/{username}'

        response = self._request('GET', location=location, jsonify=False)

        return response

    @allure.step('ApiClient: get application status')
    def get_status(self):
        logger.info('get application status')

        location = '/status'

        response = self._request('GET', location=location, jsonify=False)

        return response


class MockClient(HttpClient):

    @allure.step('MockClient: add user with username={username}, vk_id = {vk_id}')
    def add_user(self, username, vk_id):
        logger.info('MockClient: add user with username={username}, vk_id = {vk_id}')
        
        data = {}
        data['username'] = username
        data['vk_id'] = vk_id

        response = self._request('POST', location=f'/add_username', data=json.dumps(data))
        assert response == 'OK'

    @allure.step('MockClient: delete user with username={username}, vk_id = {vk_id}')
    def delete_user(self, username):
        logger.info('MockClient: delete user with username={username}, vk_id = {vk_id}')

        response = self._request('POST', location=f'/delete_username/{username}')
        assert response == 'OK'

    @allure.step('MockClient: update user with username={username}, vk_id = {vk_id}')
    def update_user(self, username, vk_id):
        logger.info('MockClient: delete user with username={username}, vk_id = {vk_id}')

        data = {}
        data['username'] = username
        data['vk_id'] = vk_id

        response = self._request('PUT', location=f'/add_username',  data=json.dumps(data))
        assert response == 'OK'