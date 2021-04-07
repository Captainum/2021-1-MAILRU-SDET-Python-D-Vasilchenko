import pytest
from _pytest.fixtures import FixtureRequest

class BaseCase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger):
        self.driver = driver
        self.config = config
        self.logger = logger
        
        self.logger.debug('Initial setup done!')