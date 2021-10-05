import pytest
from _pytest.fixtures import FixtureRequest

import logging

# from mysql.client import MySqlClient
from mysql.builder import MySQLBuilder

from builder.builder import Builder

logger = logging.getLogger('test')

class BaseCase:
    '''
        Настройка общих сущностей для API и UI тестов
    '''

    @pytest.fixture(scope='function', autouse=True)
    def setup_base(self, config, request: FixtureRequest):
        self.builder: Builder = request.getfixturevalue('builder')
        
        self.mysql_builder: MySQLBuilder = request.getfixturevalue('mysql_builder')

        self.config = config

        logger.debug('BaseCase initial setup done')