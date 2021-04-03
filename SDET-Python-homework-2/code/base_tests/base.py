import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.main_page import MainPage
class BaseCase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger):
        self.driver = driver
        self.config = config
        self.logger = logger

        self.main_page: MainPage = request.getfixturevalue('main_page')
        
        self.logger.debug('Initial setup done!')