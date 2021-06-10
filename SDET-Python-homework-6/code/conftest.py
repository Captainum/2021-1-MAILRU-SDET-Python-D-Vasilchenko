import pytest
import os

from mysql.client import MysqlClient

@pytest.fixture(scope='session')
def mysql_client():
    mysql_client = MysqlClient(user='root', password='pass', db_name='TEST_SQL')
    mysql_client.connect()
    yield mysql_client

    mysql_client.connection.close()


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        mysql_client = MysqlClient(user='root', password='pass', db_name='TEST_SQL')
        mysql_client.recreate_db()

        mysql_client.connect()
        mysql_client.create_total_requests()
        mysql_client.create_total_requests_type()
        mysql_client.create_top_requests_url()
        mysql_client.create_top_requests_size_cli()
        mysql_client.create_top_requests_serv()

        mysql_client.connection.close()


def pytest_addoption(parser):
    parser.addoption('--log_root', default='./')


@pytest.fixture(scope='session')
def config(request):
    log_root = request.config.getoption('--log_root')
    return {'log_root': os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), log_root)}