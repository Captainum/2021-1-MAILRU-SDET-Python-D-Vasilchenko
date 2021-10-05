import requests

import settings
from mock.flask_mock import SURNAME_DATA

from client.client import ClientSocket
from client.response_handler import ResponseHandler

import socket
import json
import pytest

class TestApp:
    url = f'http://{settings.APP_HOST}:{settings.APP_PORT}'

    def test_add_get_user(self):
        resp = requests.post(f'{self.url}/add_user', json={'name': 'Ilya'})
        user_id_from_add = resp.json()['user_id']

        resp = requests.get(f'{self.url}/get_user/Ilya')
        user_id_from_get = resp.json()['user_id']

        assert user_id_from_add == user_id_from_get


    def test_get_non_existent_user(self):
        resp = requests.get(f'{self.url}/get_user/dnsfndksfnkjsdnfjkdsjkfnsd')
        assert resp.status_code == 404


    def test_add_existent_user(self):
        requests.post(f'{self.url}/add_user', json={'name': 'Ilya1'})
        resp = requests.post(f'{self.url}/add_user', json={'name': 'Ilya1'})
        assert resp.status_code == 400


    def test_get_age(self):
        requests.post(f'{self.url}/add_user', json={'name': 'Vasya'})

        resp = requests.get(f'{self.url}/get_user/Vasya')

        assert isinstance(resp.json()['age'], int)
        assert 0 <= resp.json()['age'] <= 100


    def test_has_surname(self):
        SURNAME_DATA['Olya'] = 'Zaitceva'

        requests.post(f'{self.url}/add_user', json={'name': 'Olya'})

        resp = requests.get(f'{self.url}/get_user/Olya')
        assert resp.json()['surname'] == 'Zaitceva'


    def test_has_not_surname(self):
        requests.post(f'{self.url}/add_user', json={'name': 'Sveta'})

        resp = requests.get(f'{self.url}/get_user/Sveta')
        assert resp.json()['surname'] == None

    
    def test_by_socket(self):
        requests.post(f'{self.url}/add_user', json={'name': 'Egor'})

        host = settings.APP_HOST
        port = int(settings.APP_PORT)
        location = '/get_user/Egor'
        client = ClientSocket(socket.AF_INET, socket.SOCK_STREAM)

        data = client.get(url=self.url, location='/get_user/Egor')
        
        assert json.loads(data['data'])['age'] > 0


class TestMock:

    url = f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}'

    @pytest.fixture(scope='function', autouse=True)
    def setup_client(self, client_socket, response_handler):
        self.client: ClientSocket = client_socket(socket.AF_INET, socket.SOCK_STREAM)

    @pytest.fixture(scope='function')
    def setup_filled(self, builder):
        self.name, self.surname = builder.random_person()
        SURNAME_DATA[self.name] = self.surname
        
        yield
        
        if SURNAME_DATA.get(self.name):
            SURNAME_DATA.pop(self.name)

    @pytest.fixture(scope='function')
    def setup_not_filled(self, builder):
        self.name, self.surname = builder.random_person()
        
        yield
        
        if SURNAME_DATA.get(self.name):
            SURNAME_DATA.pop(self.name)


    def test_mock_get_surname(self, setup_filled):

        location = f'/get_surname/{self.name}'

        response = self.client.get(url=self.url, location=location)
        
        assert response['code'] == 200
        assert json.loads(response['data'])[0] == self.surname

    def test_mock_get_surname_negative(self, setup_not_filled):
        location = f'/get_surname/{self.name}'

        response = self.client.get(url=self.url, location=location)
        
        assert response['code'] == 404
        assert json.loads(response['data'])[0] == f'Surname for user {self.name} not found'

    def test_mock_delete_surname(self, setup_filled):
    
        location = f'/delete_surname/{self.name}'

        response = self.client.delete(url=self.url, location=location)

        assert response['code'] == 200
        assert json.loads(response['data'])[0] == 'Deleted'

    def test_mock_delete_surname_negative(self, setup_not_filled):
        location = f'/delete_surname/{self.name}'

        response = self.client.delete(url=self.url, location=location)

        assert response['code'] == 404
        assert json.loads(response['data'])[0] == f'Surname for user {self.name} not found'
        

    def test_mock_post_surname(self, setup_not_filled):
        
        location = '/add_surname'
        
        data = {self.name: self.surname}
        
        response = self.client.post(url=self.url, location=location, data=data)

        assert response['code'] == 200
        assert json.loads(response['data'])[self.name] == self.surname

    def test_mock_post_surname_negative(self, setup_filled):

        location = '/add_surname'
        
        data = {self.name: self.surname}
        
        response = self.client.post(url=self.url, location=location, data=data)

        assert response['code'] == 406
        assert json.loads(response['data'])[0] == f'Name {self.name} already has a surname'

    def test_mock_put_surname(self, setup_filled):
        
        location = '/update_surname'
        
        data = {self.name: self.surname}
        
        response = self.client.put(url=self.url, location=location, data=data)

        assert response['code'] == 200
        assert json.loads(response['data'])[0] == 'Updated'

    def test_mock_put_surname_negative(self, setup_not_filled):
        location = '/update_surname'
        
        data = {self.name: self.surname}
        
        client = ClientSocket(socket.AF_INET, socket.SOCK_STREAM)

        response = self.client.put(url=self.url, location=location, data=data)

        assert response['code'] == 404
        assert json.loads(response['data'])[0] == f'Surname for user {self.name} not found'