import logging
import os
import shutil
import signal
import subprocess
import time
from copy import copy
import pytest

import requests
from requests.exceptions import ConnectionError

import settings

from client.client import ClientSocket
from client.response_handler import ResponseHandler
from builder.builder import Builder

repo_root = os.path.abspath(os.path.join(__file__, os.pardir))  # Требуется в хуках, поэтому не выносим в фикстуру


@pytest.fixture(scope='function')
def client_socket():
    return ClientSocket

@pytest.fixture(scope='function')
def response_handler():
    return ResponseHandler

@pytest.fixture(scope='function')
def builder():
    return Builder


@pytest.fixture(scope='session')
def client_logger_dir(request):
    client_logger_dir = os.path.join(request.config.base_test_dir, 'client_log')
    os.makedirs(client_logger_dir)
    return client_logger_dir


@pytest.fixture(scope='session', autouse=True)
def logger_client(client_logger_dir):
    log_file = os.path.join(client_logger_dir, 'client.log')

    file_handler = logging.FileHandler(log_file, 'w')

    log = logging.getLogger('client_logger')
    log.propagate = False
    log.setLevel(logging.INFO)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()


def start_server(exec_type, exec_name, config):
    exec_path = os.path.join(repo_root, exec_type, exec_name)

    exec_out = open(f'/tmp/{exec_name}_stdout.log', 'w')
    exec_err = open(f'/tmp/{exec_name}_stderr.log', 'w')

    env = copy(os.environ)
    env['APP_HOST'] = settings.APP_HOST
    env['APP_PORT'] = settings.APP_PORT

    env['STUB_HOST'] = settings.STUB_HOST
    env['STUB_PORT'] = settings.STUB_PORT

    env['MOCK_HOST'] = settings.MOCK_HOST
    env['MOCK_PORT'] = settings.MOCK_PORT

    proc = subprocess.Popen(['python3.8', exec_path], stdout=exec_out, stderr=exec_err, env=env)

    if exec_type == 'app':
        config.app_proc = proc
        config.app_out = exec_out
        config.app_err = exec_err
    elif exec_type == 'stub':
        config.stub_proc = proc
        config.stub_out = exec_out
        config.stub_err = exec_err
        

def check_connection(host: str, port: str, timeout=5):
    started = False
    st = time.time()
    while time.time() - st <= timeout:
        try:
            requests.get(f'http://{host}:{port}')
            started = True
            break
        except ConnectionError:
            pass

    if not started:
        raise RuntimeError(f'App did not started in {timeout}s!')


def start_app(config):
    start_server('app', 'app.py', config)

    check_connection(settings.APP_HOST, settings.APP_PORT)


def start_stub(config):
    # start_server('stub', 'simple_http_server_stub.py', config)
    start_server('stub', 'flask_stub.py', config)

    check_connection(settings.STUB_HOST, settings.STUB_PORT)


def start_mock():
    from mock import flask_mock
    flask_mock.run_mock()

    check_connection(settings.MOCK_HOST, settings.MOCK_PORT)


def pytest_configure(config):
    base_test_dir = '/tmp/tests'

    if not hasattr(config, 'workerinput'):
        start_mock()
        start_stub(config)
        start_app(config)

        if os.path.exists(base_test_dir):
            shutil.rmtree(base_test_dir)
        os.makedirs(base_test_dir)

    config.base_test_dir = base_test_dir


def stop_app(config):
    config.app_proc.send_signal(signal.SIGINT)
    exit_code = config.app_proc.wait()

    config.app_out.close()
    config.app_err.close()

    assert exit_code == 0


def stop_stub(config):
    config.stub_proc.send_signal(signal.SIGINT)
    config.stub_proc.wait()

    config.stub_out.close()
    config.stub_err.close()


def stop_mock():
    requests.get(f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}/shutdown')


def pytest_unconfigure(config):
    if not hasattr(config, 'workerinput'):
        stop_app(config)
        stop_stub(config)
        stop_mock()
