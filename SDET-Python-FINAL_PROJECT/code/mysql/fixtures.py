import pytest

from mysql.client import MySqlClient
from mysql.builder import MySQLBuilder

@pytest.fixture(scope='session')
def mysql_client(config):
    user = config['mysql_user']
    password = config['mysql_password']
    db_name = config['mysql_db_name']
    host = config['mysql_host']
    port = config['mysql_port']

    mysql_client = MySqlClient(user=user, password=password, db_name=db_name, host=host, port=port)
    mysql_client.connect()
    
    yield mysql_client
    
    mysql_client.connection.close()


@pytest.fixture(scope='session')
def mysql_builder(mysql_client):
    return MySQLBuilder(mysql_client)