import pytest
import os
import sys

import logging

from builder.builder import Builder

from api.fixtures import *
from mysql.fixtures import *
from ui.fixtures import *

# APP_HOST = '127.0.0.1'

def pytest_addoption(parser):
    parser.addoption('--mysql_user', default='test_qa')
    parser.addoption('--mysql_password', default='qa_test')
    parser.addoption('--mysql_db_name', default='test')
    parser.addoption('--mysql_host', default='mysql')
    parser.addoption('--mysql_port', default=3306)

    parser.addoption('--app_host', default='myapp')
    parser.addoption('--app_port', default=7080)

    parser.addoption('--vk_host', default='vk_api')
    parser.addoption('--vk_port', default=8083)

    parser.addoption('--browser', default='chrome')
    parser.addoption('--selenoid', action='store_true')
    parser.addoption('--vnc', action='store_true')

    parser.addoption('--debug_log', action='store_true')


@pytest.fixture(scope='session')
def config(request):
    mysql_user = request.config.getoption('--mysql_user')
    mysql_password = request.config.getoption('--mysql_password')
    mysql_db_name = request.config.getoption('--mysql_db_name')
    mysql_host = request.config.getoption('--mysql_host')
    mysql_port = request.config.getoption('--mysql_port')

    app_host = request.config.getoption('--app_host')   
    app_port = request.config.getoption('--app_port')   

    vk_host = request.config.getoption('--vk_host')
    vk_port = request.config.getoption('--vk_port')

    if request.config.getoption('--selenoid'):
        # selenoid = 'http://127.0.0.1:4444'
        selenoid = 'http://selenoid:4444'
        if request.config.getoption('--vnc'):
            vnc = True
        else:
            vnc = False
    else:
        selenoid = None
        vnc = False
    
    browser = request.config.getoption('--browser')


    debug_log = request.config.getoption('--debug_log')

    return {'mysql_user': mysql_user,
            'mysql_password': mysql_password,
            'mysql_db_name': mysql_db_name,
            'mysql_host': mysql_host,
            'mysql_port': mysql_port,
            'app_host': app_host,
            'app_port': app_port,
            'url': f'http://{app_host}:{app_port}',
            'vk_host': vk_host,
            'vk_port': vk_port,
            'browser': browser,
            'selenoid': selenoid,
            'vnc': vnc,
            'debug_log': debug_log
            }


@pytest.fixture(scope='session')
def builder():
    return Builder


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.pardir))


@pytest.fixture(scope='function')
def test_dir(request):
    test_name = request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_')
    test_dir = os.path.join(request.config.base_test_dir, test_name)
    os.makedirs(test_dir)
    return test_dir


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_test_dir = 'C:\\tests'
    else:
        base_test_dir = '/tmp/tests'

    if not hasattr(config, 'workerinput'):
        if os.path.exists(base_test_dir):
            shutil.rmtree(base_test_dir)
        os.makedirs(base_test_dir)

    # save to config for all workers
    config.base_test_dir = base_test_dir


@pytest.fixture(scope='function', autouse=True)
def logger(test_dir, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)-15s - %(levelname)-6s - %(message)s')
    log_file = os.path.join(test_dir, 'test.log')

    log_level = logging.DEBUG if config['debug_log'] else logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()

    with open(log_file, 'r') as f:
        allure.attach(f.read(), 'test.log', attachment_type=allure.attachment_type.TEXT)