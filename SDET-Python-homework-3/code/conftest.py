import pytest
import os

from api.client import ApiClient
from utils.builder import Builder

@pytest.fixture(scope='function')
def api_client(config):
    return ApiClient(config)

def pytest_addoption(parser):
    parser.addoption('--url', default='https://target.my.com/')
    parser.addoption('--pictures_root', default='pictures')
    parser.addoption('--requests_data_root', default='requests_data')
    parser.addoption('--credentials_root', default='utils')

@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    pictures_root = request.config.getoption('--pictures_root')
    requests_data_root = request.config.getoption('--requests_data_root')
    credentials_root = request.config.getoption('--credentials_root')
    return {'url': url, 'pictures_root': pictures_root, 'requests_data_root': requests_data_root, 'credentials_root': credentials_root}

@pytest.fixture(scope='session')
def credentials(config):
    with open(os.path.join(config['credentials_root'], 'user'), 'r') as f:
        user = f.readline().strip()
        password = f.readline().strip()

    return user, password

@pytest.fixture(scope='function')
def builder():
    return Builder